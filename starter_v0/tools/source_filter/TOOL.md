---
name: source_filter
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [items, allowed_domains, blocked_domains, top_k, require_url]
outputs: [items, kept_count, dropped_count]
side_effect: false
---
# source_filter

Filters, deduplicates, and ranks already-collected research items by source rules. This tool is useful after search tools return many results and before formatting a final digest.

## When to use

- Use after `lookup`, `fetch`, `papers`, `social_search`, or `timeline` when the user asks to keep only certain sources.
- Use when the user asks to exclude sources, remove duplicates, require links, or keep only the top N results.
- Use before `format` when the final digest should be based on filtered sources.
- Do not use for searching the web or reading URLs; collect items first with another tool.

## Inputs

- `items`: list of result objects. Each item may include `title`, `url`, `source`, `summary`, and `score`.
- `allowed_domains`: optional list of domains to keep, such as `openai.com` or `techcrunch.com`.
- `blocked_domains`: optional list of domains to remove.
- `top_k`: maximum number of items to return.
- `require_url`: whether items without a URL should be dropped.

## Output

Returns a JSON object with:

- `items`: filtered items.
- `kept_count`: number of returned items.
- `dropped_count`: number of removed items.

## Notes

- Domain matching also accepts subdomains, so `openai.com` matches `news.openai.com`.
- Duplicate URLs are removed.
- Items with higher `score` are ranked first when scores are available.
