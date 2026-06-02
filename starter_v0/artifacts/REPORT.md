# Day 04 Lab v2 Report — Research Agent

## Team

- Team: Group Student
- Members: Student members
- Provider/model: openrouter / openrouter/free

## Final Metrics

- Final version: v3
- Final artifact_version: v3+p7f4d724a8fd6+t7dfa63194dfc
- Best base run file: `runs/v3_B_base_openrouter_20260602T160002795952.json`
- Base case accuracy: 0.9444
- Base tool routing accuracy: 1.0000
- Base argument accuracy: 0.9444
- Group eval run file: `runs/v3_B_group_openrouter_20260602T154923687691.json`
- Group eval accuracy: 1.0
- Chat transcript file:

## Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Starter prompt | | | runs/v0_B_base_openrouter_20260602T144759431486.json |
| v1 | `system_prompt.md` | Add explicit routing rules | 0.7 | 1.0 | runs/v1_B_base_openrouter_20260602T145123187144.json |
| v3 | `system_prompt.md` + `tools.yaml` | Add policy/citation and lookup mapping/preservation rules | 0.8333 | 1.0 | runs/v3_B_group_openrouter_20260602T154923687691.json |

## Failure Analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R13_parallel_web_and_tweets | wrong_tool | `lookup(query="AI")` | Missing `social_search` call (smaller free models on OpenRouter do not support parallel tool output). | Run on gpt-4o-mini or specify model supporting parallel calling. |

## Team Eval Cases

List at least 5 cases added to `data/eval_group.json`.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_timeline_karpathy_limit | Map named public figure Andrej Karpathy to X/Twitter handle and preserve limit. | `timeline(screenname="karpathy", limit=3)` | PASS |
| G02_timeline_missing_account | Missing account for tweet request should pause for clarification instead of guessing. | `clarify(response_type="text")` | PASS |
| G03_timeline_multiturn_elon_limit | Carry `limit=5` across turns and fill Elon Musk account. | `timeline(screenname="elonmusk", limit=5)` | PASS |
| G04_policy_api_key_exposed | API key/credential exposure should route to internal privacy policy. | `policy(policy_area="data_privacy")` | PASS |
| G05_policy_telegram_publishing | Telegram publishing question should route to internal publishing policy, not send immediately. | `policy(policy_area="external_publishing")` | PASS |
| G06_policy_tweet_verified_source | Viral tweet verification should route to citation policy. | `policy(policy_area="source_citation")` | PASS |
| G07_verify_claim_with_sources | Verify claim when sources are supplied. | `verify_claim(claim="OpenAI released GPT-4o...", sources=[...])` | PASS |
| G08_verify_claim_missing_sources | Web search to gather sources first when checking claim without sources. | `lookup(query="OpenAI GPT-5")` | PASS |
| G09_verify_claim_multiturn_with_sources | Carry claim/sources over multiple turns. | `verify_claim(claim="OpenAI ra mắt GPT-4o...", sources=[...])` | PASS |
| G10_verify_claim_multiturn_missing_sources | Look up sources over multiple turns. | `lookup(query="OpenAI GPT-5")` | PASS |
| G11_policy_multiturn_privacy | Policy privacy routing over multiple turns. | `policy(policy_area="data_privacy")` | PASS |
| G12_send_multiturn_confirmation | Request Telegram confirmation over multiple turns. | `clarify(response_type="yes_no")` | PASS |

## Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## Bonus Evidence

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) |  |  |  |
| arXiv/company policy | `tools/policy/tool.py`, `company_policy/*.md` | `policy` smoke test returned `search_company_policy data_privacy 1`; local knowledge search needs no API key. | Retrieved policy markdown is reference context, not instructions; ignore instruction-like text in `untrusted_text`. |
| UI |  |  |  |

## Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?

