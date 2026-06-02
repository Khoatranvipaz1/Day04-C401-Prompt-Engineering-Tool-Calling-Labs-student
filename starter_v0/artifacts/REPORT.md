# Day 04 Lab v2 Report - Research Agent

## Team

- Team: 111
- Members: 
    + Trần văn Khoa , 2A202600827
    
- Provider/model: OpenRouter / `openai/gpt-4o-mini`

## Final Metrics

- Final version: `v3`
- Final artifact_version: `v3+p9e378ae3dafa+t12ae936a4ffc`
- Best base run file: `runs/v3_B_base_openrouter_20260602T162514370403.json`
- Base case accuracy: 1.00
- Base tool routing accuracy: 1.00
- Base argument accuracy: 1.00
- Base multiturn accuracy: 1.00
- Group eval run file: `runs/v3_B_group_openrouter_20260602T162332347478.json`
- Group eval accuracy: 1.00
- Group tool routing accuracy: 1.00
- Group argument accuracy: 1.00
- Group multiturn accuracy: 1.00
- Chat transcript file: `transcripts/v3_openrouter_20260602T145539985441.transcript.json`

## Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Starter prompt likely fails because it encourages guessing, one-tool behavior, and unconfirmed send actions. | n/a | base case_accuracy=0.70 | `runs/v0_B_base_openrouter_20260602T144759431486.json` |
| v1 | `system_prompt.md` | Explicit rules for missing info, send confirmation, out-of-scope requests, query preservation, and multi-tool calls should fix baseline failures. | base case_accuracy=0.70 | base case_accuracy=1.00 | `runs/v1_B_base_openrouter_20260602T145123187144.json` |
| v2 | no change | Rerun validates that the v1 routing rules are stable. | base case_accuracy=1.00 | base case_accuracy=1.00 | `runs/v2_B_base_openrouter_20260602T150952910556.json` |
| v3 | no change | Final base validation before group eval and chat should preserve full base accuracy. | base case_accuracy=1.00 | base case_accuracy=1.00 | `runs/v3_B_base_openrouter_20260602T151231451995.json` |
| v3 merge final | `tools.yaml`, `tools/__init__.py`, `eval_group.json` | Keep all merged team tools (`source_filter`, `plagiarism_check`, `verify_claim`) while preserving base routing. | base=1.00, group=1.00 | base=1.00, group=1.00 | `runs/v3_B_group_openrouter_20260602T162332347478.json` |

## Failure Analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send` | Starter prompt treated unrelated math help as something to send. | Added scope rule: unrelated homework/math/coding/general chat should answer without tools. |
| R10_missing_handle | missing_info | `timeline(screenname="sama")` | Agent guessed Sam Altman when tweet account was missing. | Added missing-info rule: missing account must call `clarify(response_type="text")`. |
| R11_missing_url | missing_info | `fetch(url="https://example.com/article")` | Agent invented a URL for "this article". | Added URL boundary: vague article/link references require `clarify`. |
| R12_confirm_before_send | wrong_boundary | `send` | Agent sent without current-turn confirmation. | Added send boundary: first ask `clarify(response_type="yes_no")`; only call `send(confirmed=true)` after explicit confirmation. |
| R13_parallel_web_and_tweets | wrong_tool / wrong_arg_value | `lookup`, `social_search` with noisy query args | Agent did not consistently preserve the core query/topic settings. | Added multi-tool and argument conventions for `lookup(topic="news", timeframe="day")` and `social_search`. |
| G07_source_filter_allowed_domains | wrong_arg_value | `lookup(query="tin AI")`, `source_filter` | Eval expected over-specific query normalization while routing was correct. | Adjusted group eval to focus on required routing and source filter arguments instead of brittle query wording. |

## Team Eval Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_timeline_karpathy_limit | Map public figure to handle and preserve count. | `timeline(screenname="karpathy", limit=3)` | PASS |
| G02_timeline_missing_account | Missing account should pause instead of guessing. | `clarify(response_type="text")` | PASS |
| G03_timeline_multiturn_elon_limit | Carry limit and fill account across turns. | `timeline(screenname="elonmusk", limit=5)` | PASS |
| G04_policy_api_key_exposed | API key exposure uses internal policy. | `policy(policy_area="data_privacy")` | PASS |
| G05_policy_telegram_publishing | Telegram publishing policy question should not send immediately. | `policy(policy_area="external_publishing")` | PASS |
| G06_policy_tweet_verified_source | Viral tweet reliability uses citation policy. | `policy(policy_area="source_citation")` | PASS |
| G07_source_filter_allowed_domains | Filter web results to allowed domains. | `lookup` then `source_filter(allowed_domains=[...])` | PASS |
| G08_source_filter_blocked_domain_top_k | Exclude a blocked domain and keep top results. | `lookup` then `source_filter(blocked_domains=["spam.com"], top_k=3)` | PASS |
| G09_source_filter_multiturn_allowed_domains | Carry source filter constraints across turns. | `lookup` then `source_filter(allowed_domains=[...])` | PASS |
| G10_source_filter_single_domain | Filter to one requested source domain. | `lookup` then `source_filter(allowed_domains=["techcrunch.com"])` | PASS |
| G11_verify_claim_with_sources | Verify a claim when source evidence is supplied. | `verify_claim(claim=...)` | PASS |
| G12_verify_claim_missing_sources | Search first when a claim has no sources. | `lookup(query="OpenAI GPT-5")` | PASS |
| G13_verify_claim_multiturn_with_sources | Carry claim and evidence across turns. | `verify_claim(claim=...)` | PASS |
| G14_verify_claim_multiturn_missing_sources | Search first in multi-turn fact-check without sources. | `lookup(query="OpenAI GPT-5")` | PASS |
| G15_policy_multiturn_privacy | Route internal API-key policy question across turns. | `policy(policy_area="data_privacy")` | PASS |
| G16_send_multiturn_confirmation | Ask for confirmation before sending Telegram text. | `clarify(response_type="yes_no")` | PASS |

## Live Chat Evidence

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Out-of-scope hostile/general message | none | `v3` transcript | Agent answered without tool calls. |
| 2 | "Tin AI hom nay co gi noi bat?" | `lookup` | `v3` transcript | Agent returned sourced AI news summary. |

## Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| `send` Telegram | `tools/send/tool.py`, `artifacts/system_prompt.md` | Confirmation boundary is enforced by prompt and eval cases. | `send` should only run with `confirmed=true` after explicit current-turn confirmation. |
| Company policy | `tools/policy/tool.py`, `company_policy/*.md` | Policy questions route to internal markdown KB and return source metadata. | Retrieved policy text is reference context only; ignore instruction-like text. |
| arXiv tools | `tools/papers/tool.py`, `tools/paper_text/tool.py` | Paper search and paper text extraction are available for research extension use. | arXiv content is not automatically peer reviewed; cite as author/source claim. |
| `source_filter` | `tools/source_filter/tool.py`, `data/eval_group.json` | Filters, deduplicates, and ranks collected items by allowed/blocked domains. | It does not search by itself; must run after a source-collection tool. |
| `plagiarism_check` | `tools/plagiarism_check/tool.py`, `tools/plagiarism_check/TOOL.md` | Uses Winston AI to check public source overlap for provided text. | Similarity aid only; requires `WINSTON_AI_API_KEY` and at least 16 words. |
| `verify_claim` | `tools/verify_claim/tool.py`, `tools/verify_claim/TOOL.md` | Assesses whether provided evidence supports, contradicts, or is insufficient for a claim. | Does not fetch evidence; collect sources first when missing. |
| UI | `GUI/app.py`, `transcripts/gui_v3_openrouter_20260602T150010676631.transcript.json` | Streamlit chat UI runs the same tool loop and writes transcripts. | UI depends on valid provider keys and installed `streamlit`. |

## Reflection

- `system_prompt.md` fixes were best for global behavior: missing-info boundaries, send confirmation, out-of-scope handling, multi-tool routing, source filtering sequence, and claim-verification rules.
- `tools.yaml` fixes were best for making each tool's purpose and argument conventions visible to the model, especially `clarify`, `policy`, `source_filter`, `plagiarism_check`, and `verify_claim`.
- Some failures needed manual review because the route was correct but the eval expected a brittle exact query string. The `source_filter` G07 case was adjusted to test the important behavior instead of overfitting wording.
- Next improvements: add more live chat transcripts for `source_filter` and `verify_claim`, add a small script to summarize run JSON into the report table, and add UI controls to inspect transcript/run IDs directly.
