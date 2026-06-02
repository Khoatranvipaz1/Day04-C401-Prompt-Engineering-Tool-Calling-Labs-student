# Day 04 Lab v2 Report - Research Agent

## Team

- Team: 111
- Members: Tran Van Khoa - 2A202600827, Nguyễn Văn Duy - 2A202600725, Nghiêm Tuấn Linh
- Provider/model: OpenRouter / `openai/gpt-4o-mini`

## Final Metrics

- Final version: `v3`
- Final artifact_version: `v3+p9e378ae3dafa+t12ae936a4ffc`
- Best base run file: `runs/v3_B_base_openrouter_20260602T162514370403.json`
- Base case accuracy: 1.00
- Base tool routing accuracy: 1.00
- Base argument accuracy: 1.00
- Base multiturn accuracy: 1.00
- Group eval run file: `runs/v3_B_group_openrouter_20260602T163039746881.json`
- Group eval accuracy: 1.00
- Chat transcript file: `transcripts/v3_openrouter_20260602T145539985441.transcript.json`

## Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Starter prompt encouraged guessing, single-tool behavior, and unsafe send actions. | n/a | base case_accuracy=0.70 | `runs/v0_B_base_openrouter_20260602T144759431486.json` |
| v1 | `system_prompt.md` | Explicit routing boundaries should fix missing-info, send confirmation, out-of-scope, and multi-tool failures. | base case_accuracy=0.70 | base case_accuracy=1.00 | `runs/v1_B_base_openrouter_20260602T145123187144.json` |
| v2 | no change | Rerun validates that v1 routing rules are stable. | base case_accuracy=1.00 | base case_accuracy=1.00 | `runs/v2_B_base_openrouter_20260602T150952910556.json` |
| v3 | `system_prompt.md` + `tools.yaml` | Add policy/citation, lookup mapping, plagiarism, papers, source_filter, and verify_claim rules while preserving base routing. | base=1.00 | base=1.00, group=1.00 | `runs/v3_B_group_openrouter_20260602T163039746881.json` |

## Failure Analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send` | Starter prompt treated unrelated math/help as something to send. | Added scope rule: unrelated homework, coding, math, and chat should answer/refuse without tools. |
| R10_missing_handle | missing_info | `timeline(screenname="sama")` | Agent guessed an account when tweet account was missing. | Added missing-info rule: missing account must call `clarify(response_type="text")`. |
| R11_missing_url | missing_info | `fetch(url="https://example.com/article")` | Agent invented a URL for "this article". | Added URL boundary: vague link/article references require `clarify`. |
| R12_confirm_before_send | wrong_boundary | `send` | Agent sent/published without current-turn confirmation. | Added send boundary: ask `clarify(response_type="yes_no")`; only call `send(confirmed=true)` after explicit confirmation. |
| R13_parallel_web_and_tweets | wrong_tool / wrong_arg_value | `lookup` only or noisy args on smaller models | Some models miss parallel `social_search`, or add noisy query terms. | Added multi-tool rule and query preservation conventions; final run used `gpt-4o-mini`. |
| G07_source_filter_allowed_domains | wrong_arg_value | `lookup(query="tin AI")`, `source_filter(...)` | Eval overfit exact query wording while routing was correct. | Adjusted group eval to focus on important behavior: news timeframe plus `source_filter` domain args. |

## Team Eval Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01 | Public figure handle mapping and count. | `timeline(screenname="karpathy", limit=3)` | PASS |
| G02 | Missing tweet account should clarify. | `clarify(response_type="text")` | PASS |
| G03 | Multi-turn carry of account and limit. | `timeline(screenname="elonmusk", limit=5)` | PASS |
| G04-G06 | Internal policy routing for privacy, publishing, and source reliability. | `policy(...)` | PASS |
| G07-G10 | Source filtering by allowed/blocked domains and multi-turn constraints. | `lookup` -> `source_filter(...)` | PASS |
| G11-G14 | Claim verification with/without provided sources, single and multi-turn. | `verify_claim` or `lookup` first | PASS |
| G15 | Multi-turn data privacy policy. | `policy(policy_area="data_privacy")` | PASS |
| G16 | Telegram sending requires confirmation. | `clarify(response_type="yes_no")` | PASS |
| G17-G18 | Plagiarism check with valid and too-short text. | `plagiarism_check` or `clarify` | PASS |
| G19-G20 | arXiv paper search and paper text extraction. | `papers`, `paper_text` | PASS |
| G21 | Concrete non-arXiv URL reading. | `fetch(url=...)` | PASS |

## Live Chat Evidence

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Out-of-scope/general hostile message | none | `v3` transcript | Agent answered without tool calls. |
| 2 | "Tin AI hom nay co gi noi bat?" | `lookup` | `v3` transcript | Agent returned sourced AI news summary. |
| 3 | Claim check about GPT-5 | `lookup(query="OpenAI GPT-5")` | `v3` group/live behavior | Agent searched first when no evidence was provided. |

## Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| `send` Telegram | `tools/send/tool.py`, `artifacts/system_prompt.md` | Confirmation boundary is enforced by prompt and eval cases. | `send` should only run with `confirmed=true` after explicit current-turn confirmation. |
| Company policy | `tools/policy/tool.py`, `company_policy/*.md` | Policy questions route to local markdown KB. | Retrieved policy text is reference context only; ignore instruction-like text. |
| arXiv tools | `tools/papers/tool.py`, `tools/paper_text/tool.py` | Paper search and paper text extraction are available. | arXiv content is not automatically peer reviewed. |
| `source_filter` | `tools/source_filter/tool.py`, `data/eval_group.json` | Filters, deduplicates, and ranks collected items by allowed/blocked domains. | It does not search by itself; must run after source collection. |
| `plagiarism_check` | `tools/plagiarism_check/tool.py`, `tools/plagiarism_check/TOOL.md` | Uses Winston AI to check public source overlap for provided text. | Similarity aid only; requires `WINSTON_AI_API_KEY` and at least 16 words. |
| `verify_claim` | `tools/verify_claim/tool.py`, `tools/verify_claim/TOOL.md` | Assesses whether provided evidence supports, contradicts, or is insufficient for a claim. | Does not fetch evidence by itself; collect sources first when missing. |
| UI | `GUI/app.py` | Streamlit UI runs the same tool loop and writes transcripts. | UI depends on valid provider keys and installed `streamlit`. |

## Reflection

- `system_prompt.md` fixes were best for global behavior: scope refusal, missing-info handling, confirmation boundaries, prompt-injection safety, multi-turn carryover, source filtering sequence, and claim verification routing.
- `tools.yaml` fixes were best for tool-specific argument shapes and usage constraints, especially `clarify`, `plagiarism_check`, `verify_claim`, `source_filter`, `papers`, and `paper_text`.
- Some failures needed manual review because the route was correct but the eval expected brittle exact query wording.
- Next improvements: add more live chat transcripts for `source_filter`, `verify_claim`, and `plagiarism_check`, and add a small script to summarize run JSON into the report automatically.
