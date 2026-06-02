---
name: plagiarism_check
track: group
kind: live_api
provider: Winston AI
requires_env: [WINSTON_AI_API_KEY]
inputs: [text]
outputs: [status, results_count, matches, credits_used, credits_remaining]
side_effect: false
---
# plagiarism_check

Checks a text for public source overlap using Winston AI's plagiarism API.
This is an originality/similarity aid, not a definitive plagiarism verdict.

The Winston AI plagiarism endpoint requires at least 16 words and at most
20,000 words in each request.

The implementation accepts either `WINSTON_API_KEY` or `WINSTON_AI_API_KEY`.
