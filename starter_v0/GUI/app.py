from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chat import (  # noqa: E402
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from env_loader import load_lab_env  # noqa: E402
from providers import make_provider  # noqa: E402
from tools import load_tool_declarations, to_openai_tools  # noqa: E402
from versioning import artifact_version_dict, build_artifact_version  # noqa: E402


ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
load_lab_env(ROOT)


def json_block(value: Any, *, max_chars: int = 8000) -> str:
    text = json.dumps(value, ensure_ascii=False, indent=2, default=str)
    if len(text) > max_chars:
        return text[:max_chars] + "\n...<truncated>"
    return text


def init_transcript(*, provider_name: str, model: str | None, version: str, history_window: int, max_tool_rounds: int) -> None:
    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    artifact_version = build_artifact_version(version, system_prompt_path, tools_path)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([
        "gui",
        safe_slug(version),
        safe_slug(provider_name),
        timestamp,
    ])
    transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
    st.session_state.transcript_path = transcript_path
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model,
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
        "ui": "streamlit",
    }
    st.session_state.messages = []
    st.session_state.history = []
    st.session_state.turn_index = 0


@st.cache_resource(show_spinner=False)
def load_runtime(provider_name: str, model: str | None) -> tuple[Any, list[dict[str, Any]], str, str]:
    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(tools_path)
    openai_tools = to_openai_tools(tool_declarations)
    provider = make_provider(provider_name)
    selected_model = model or getattr(provider, "default_model", "")
    return provider, openai_tools, system_prompt, selected_model


st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="wide")

st.title("Research Agent")

with st.sidebar:
    st.header("Session")
    provider_name = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini"], index=0)
    model_value = st.text_input("Model", value="openrouter/free" if provider_name == "openrouter" else "")
    model = model_value.strip() or None
    version = st.text_input("Version", value="v3").strip() or "v3"
    history_window = st.number_input("History window", min_value=0, max_value=20, value=5, step=1)
    max_tool_rounds = st.number_input("Max tool rounds", min_value=1, max_value=10, value=4, step=1)

    settings = {
        "provider": provider_name,
        "model": model,
        "version": version,
        "history_window": int(history_window),
        "max_tool_rounds": int(max_tool_rounds),
    }

    if "settings" not in st.session_state or st.session_state.settings != settings:
        st.session_state.settings = settings
        init_transcript(
            provider_name=provider_name,
            model=model,
            version=version,
            history_window=int(history_window),
            max_tool_rounds=int(max_tool_rounds),
        )

    if st.button("New chat", use_container_width=True):
        load_runtime.clear()
        init_transcript(
            provider_name=provider_name,
            model=model,
            version=version,
            history_window=int(history_window),
            max_tool_rounds=int(max_tool_rounds),
        )
        st.rerun()

    transcript_path = st.session_state.get("transcript_path")
    if transcript_path:
        st.caption(f"Transcript: `{transcript_path.relative_to(ROOT)}`")


provider, openai_tools, system_prompt, selected_model = load_runtime(provider_name, model)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("tool_events"):
            with st.expander("Tool events"):
                st.code(json_block(message["tool_events"]), language="json")


user_text = st.chat_input("Nhập yêu cầu nghiên cứu...")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    st.session_state.turn_index += 1
    turn_record: dict[str, Any] = {
        "turn_index": st.session_state.turn_index,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, int(history_window)),
        {"role": "user", "content": user_text},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=model,
                    max_tool_rounds=int(max_tool_rounds),
                )
                turn_record.update(result)
                assistant_text = result["assistant_text"]
                st.markdown(assistant_text)
                tool_events = result.get("tool_events") or []
                if tool_events:
                    with st.expander("Tool events"):
                        st.code(json_block(tool_events), language="json")
                st.session_state.history.append({"role": "user", "content": user_text})
                st.session_state.history.append({"role": "assistant", "content": assistant_text})
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tool_events": tool_events,
                })
            except Exception as exc:
                assistant_text = f"Provider error: {type(exc).__name__}: {exc}"
                turn_record.update({
                    "status": "provider_error",
                    "assistant_text": assistant_text,
                    "error": assistant_text,
                })
                st.error(assistant_text)
                st.session_state.messages.append({"role": "assistant", "content": assistant_text})

    turn_record["ended_at"] = now_iso()
    st.session_state.transcript["turns"].append(turn_record)
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)
