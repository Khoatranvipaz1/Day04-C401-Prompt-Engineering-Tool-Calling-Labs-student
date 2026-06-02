---
name: lookup
track: core
kind: live_api
provider: Tavily
requires_env: [TAVILY_API_KEY]
inputs: [query, topic, timeframe, max_results]
outputs: [items]
side_effect: false
---
# lookup

Searches the public web with Tavily and returns a compact list of relevant results. Use this for current or general internet research when the user does not provide a specific URL.

## When to use

- Use when the user asks to research a topic on the web.
- Use when the user asks for current news, recent developments, market information, announcements, or public facts that may have changed.
- Use when the user asks for sources or links but has not provided a URL.
- Do not use for reading a specific URL; use `fetch` instead.
- Do not use for social-media posts; use `timeline` or `social_search`.
- Do not use for internal company policy; use `policy`.
- Do not use for arXiv papers; use `papers`.

## Inputs

- `query`: the web search query.
- `topic`: `general` for broad web search, or `news` for news-oriented queries.
- `timeframe`: one of `day`, `week`, `month`, or `year`.
- `max_results`: maximum number of returned results.

## Output

Returns a JSON object with:

- `items`: result objects containing `title`, `url`, `source`, `summary`, and `score`.

## Notes

- Prefer `topic: news` for "latest", "recent", "today", "this week", or breaking-news requests.
- Prefer the narrowest useful `timeframe`; for example, use `day` for today's news and `week` for this week's developments.
- After `lookup`, use `format` if the user asked for a polished digest or Markdown report.
