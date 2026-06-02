from __future__ import annotations

import os
import re
from typing import Any

import requests

from tools._shared import TIMEOUT, err


API_URL = "https://api.gowinston.ai/v1/plagiarism"
MIN_WORDS = 16
MAX_WORDS = 20_000


def _word_count(text: str) -> int:
    return len(re.findall(r"\S+", text or ""))


def _normalize_results(results: Any) -> list[dict[str, Any]]:
    if isinstance(results, dict):
        iterable = results.values()
    elif isinstance(results, list):
        iterable = results
    else:
        iterable = []

    matches: list[dict[str, Any]] = []
    for item in iterable:
        if not isinstance(item, dict):
            continue
        matches.append({
            "title": item.get("title") or "",
            "url": item.get("url") or "",
            "date": item.get("date") or "",
            "excerpts": item.get("excerpts") or {},
        })
    return matches


def check_plagiarism(text: str = "") -> dict[str, Any]:
    try:
        token = os.getenv("WINSTON_API_KEY") or os.getenv("WINSTON_AI_API_KEY")
        if not token:
            raise RuntimeError("Missing WINSTON_API_KEY / WINSTON_AI_API_KEY env var")

        clean_text = (text or "").strip()
        words = _word_count(clean_text)
        if words < MIN_WORDS:
            raise ValueError(f"Winston AI plagiarism check requires at least {MIN_WORDS} words; got {words}")
        if words > MAX_WORDS:
            raise ValueError(f"Winston AI plagiarism check allows at most {MAX_WORDS} words; got {words}")

        response = requests.post(
            API_URL,
            json={"text": clean_text},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        matches = _normalize_results(data.get("results"))
        return {
            "tool": "plagiarism_check",
            "status": data.get("status", response.status_code),
            "results_count": data.get("results_count", len(matches)),
            "matches": matches,
            "credits_used": data.get("credits_used"),
            "credits_remaining": data.get("credits_remaining"),
            "note": "Similarity/originality aid only; not a definitive plagiarism verdict.",
        }
    except Exception as exc:
        return err("plagiarism_check", exc)
