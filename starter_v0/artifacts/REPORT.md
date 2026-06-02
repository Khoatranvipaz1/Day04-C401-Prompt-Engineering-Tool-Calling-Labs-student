# Day 04 Lab v2 Report — Research Agent

## Team

- Team:
- Members:
- Provider/model:

## Final Metrics

- Final version:
- Final artifact_version:
- Best base run file:
- Base case accuracy:
- Base tool routing accuracy:
- Base argument accuracy:
- Group eval run file: `runs/v3_B_group_openrouter_20260602T135724636098.json`
- Group eval accuracy: 1.0
- Chat transcript file:

## Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 | `tools.yaml` | Clearer `timeline` and `policy` descriptions improve routing for owned tools. |  | 0.3333 | `runs/v1_B_group_openrouter_20260602T135158413089.json` |
| v2 | `system_prompt.md` | Replacing the starter prompt's guessing/posting behavior improves policy routing and missing-info handling. | 0.3333 | 0.8333 | `runs/v2_B_group_openrouter_20260602T135512858601.json` |
| v3 | `system_prompt.md` + `tools.yaml` | Clarify declaration plus stricter missing-info rule makes missing tweet account call `clarify`. | 0.8333 | 1.0 | `runs/v3_B_group_openrouter_20260602T135724636098.json` |

## Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

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

