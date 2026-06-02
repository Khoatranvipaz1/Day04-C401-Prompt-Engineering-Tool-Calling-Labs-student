---
name: verify_claim
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [claim, sources, strictness]
outputs: [verdict, confidence, evidence, missing_evidence]
side_effect: false
---
# verify_claim

Checks whether provided source snippets support or contradict a claim. This tool
does not search the web by itself; use `lookup`, `fetch`, `papers`, or
`paper_text` first when evidence is missing.

## When to use

- Use after source collection when the user asks to verify, fact-check, or assess
  whether a claim is supported.
- Use when the user provides both a claim and source snippets/items.
- Do not use as the first step for a claim with no evidence; collect sources
  first.

## Inputs

- `claim`: the claim to assess.
- `sources`: list of source objects. Each item may include `title`, `url`,
  `source`, and `summary`.
- `strictness`: `quick`, `standard`, or `strict`.

## Output

Returns a JSON object with `verdict`, `confidence`, supporting/contradicting
evidence notes, and missing evidence.
