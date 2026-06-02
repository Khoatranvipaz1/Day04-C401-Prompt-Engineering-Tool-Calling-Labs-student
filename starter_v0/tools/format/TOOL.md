---
name: format
track: core
kind: local_formatter
provider: local
requires_env: []
inputs: [items, template, headline]
outputs: [markdown, item_count]
side_effect: false
---
# format

Renders already-collected research items into a Markdown digest. This tool does not search, fetch, or create new facts; it only presents items that are already available from previous tool results or user-provided data.

## When to use

- Use after `lookup`, `fetch`, `timeline`, `social_search`, `policy`, `papers`, or `paper_text` when the user asks for a digest, report, recap, newsletter, thread, or clean Markdown output.
- Use when the user asks to organize existing items into sections, bullets, a short brief, or a Vietnamese daily AI digest.
- Do not use as a general writing or rewriting tool when there are no structured `items` to format.
- Do not call this tool before collecting the source items that need to be formatted.

## Inputs

- `items`: list of objects to render. Each item may include `title`, `url`, `source`, `summary`, and `section`.
- `template`: one of `brief`, `sections`, `bullets`, `thread`, or `daily_ai_vn`.
- `headline`: optional title for the digest.

## Output

Returns a JSON object with:

- `markdown`: the rendered Markdown text.
- `item_count`: number of input items rendered.

## Notes

- Choose `brief` for a short top-5 summary.
- Choose `sections` when items have categories or should be grouped.
- Choose `bullets` for a simple list.
- Choose `thread` for numbered social-post style output.
- Choose `daily_ai_vn` for a Vietnamese daily AI/news digest.
