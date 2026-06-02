from __future__ import annotations

import re
from typing import Any

from tools._shared import domain, err


def _clean_domain(value: str) -> str:
    value = (value or "").strip().lower()
    if value.startswith("www."):
        value = value[4:]
    return value


def _matches(candidate: str, rules: list[str]) -> bool:
    candidate = _clean_domain(candidate)
    for rule in rules:
        rule = _clean_domain(rule)
        if candidate == rule or candidate.endswith("." + rule):
            return True
    return False


def _domain_list(value: list[str] | str | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [part for part in re.split(r"[\s,;]+", value.strip()) if part]
    return value


def filter_sources(
    items: list[dict[str, Any]] | None = None,
    allowed_domains: list[str] | str | None = None,
    blocked_domains: list[str] | str | None = None,
    top_k: int = 5,
    require_url: bool = True,
) -> dict[str, Any]:
    try:
        source_items = items or []
        allowed_domains = _domain_list(allowed_domains)
        blocked_domains = _domain_list(blocked_domains)
        allowed = [_clean_domain(item) for item in (allowed_domains or []) if item]
        blocked = [_clean_domain(item) for item in (blocked_domains or []) if item]
        limit = max(0, int(top_k or 0))

        kept: list[dict[str, Any]] = []
        seen_urls: set[str] = set()

        for item in source_items:
            url = (item.get("url") or "").strip()
            item_domain = _clean_domain(item.get("source") or domain(url))

            if require_url and not url:
                continue
            if url and url in seen_urls:
                continue
            if allowed and not _matches(item_domain, allowed):
                continue
            if blocked and _matches(item_domain, blocked):
                continue

            copied = dict(item)
            copied["source"] = copied.get("source") or item_domain
            kept.append(copied)
            if url:
                seen_urls.add(url)

        kept.sort(key=lambda item: item.get("score") if item.get("score") is not None else 0, reverse=True)
        if limit:
            kept = kept[:limit]

        return {
            "tool": "filter_sources",
            "items": kept,
            "kept_count": len(kept),
            "dropped_count": max(0, len(source_items) - len(kept)),
            "allowed_domains": allowed,
            "blocked_domains": blocked,
            "require_url": bool(require_url),
        }
    except Exception as exc:
        return err("filter_sources", exc)
