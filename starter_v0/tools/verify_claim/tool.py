from __future__ import annotations

from typing import Any

from tools._shared import domain, err, terms


NEGATION_TERMS = {
    "false", "fake", "incorrect", "not", "no", "denied", "deny", "contradict", "contradicted",
    "khong", "không", "sai", "gia", "giả", "phu nhan", "phủ nhận", "chua", "chưa",
}


def _source_label(item: dict[str, Any]) -> str:
    source = item.get("source") or domain(str(item.get("url") or ""))
    return source or str(item.get("title") or "source")


def _text(item: dict[str, Any]) -> str:
    return " ".join(str(item.get(key) or "") for key in ("title", "summary", "content", "facts"))


def _evidence_item(item: dict[str, Any], claim_terms: set[str]) -> dict[str, Any] | None:
    text = _text(item)
    source_terms = terms(text)
    overlap = sorted(claim_terms & source_terms)
    if not overlap:
        return None

    lowered = text.lower()
    contradicts = any(term in lowered for term in NEGATION_TERMS)
    note_text = text.strip().replace("\n", " ")
    if len(note_text) > 280:
        note_text = note_text[:277] + "..."
    return {
        "title": item.get("title") or "",
        "source": _source_label(item),
        "url": item.get("url") or "",
        "supports": not contradicts,
        "contradicts": contradicts,
        "matched_terms": overlap[:12],
        "note": note_text,
    }


def verify_claim(claim: str = "", sources: list[dict[str, Any]] | None = None, strictness: str = "standard") -> dict[str, Any]:
    try:
        sources = sources or []
        claim_terms = terms(claim)
        if not claim.strip():
            return {
                "tool": "verify_claim",
                "claim": claim,
                "verdict": "needs_more_sources",
                "confidence": "low",
                "evidence": [],
                "missing_evidence": ["claim"],
            }

        evidence = [
            item for item in (_evidence_item(source, claim_terms) for source in sources)
            if item is not None
        ]
        supported = [item for item in evidence if item["supports"]]
        contradicted = [item for item in evidence if item["contradicts"]]

        strict = (strictness or "standard").strip().lower()
        required_support = 1 if strict == "quick" else 2 if strict == "standard" else 3

        if contradicted and not supported:
            verdict = "contradicted"
            confidence = "medium" if len(contradicted) >= required_support else "low"
        elif len(supported) >= required_support and not contradicted:
            verdict = "supported"
            confidence = "high" if len(supported) > required_support else "medium"
        elif supported and contradicted:
            verdict = "unclear"
            confidence = "low"
        elif supported:
            verdict = "needs_more_sources"
            confidence = "low"
        else:
            verdict = "needs_more_sources"
            confidence = "low"

        missing_evidence: list[str] = []
        if not sources:
            missing_evidence.append("sources")
        if verdict == "needs_more_sources":
            missing_evidence.append(f"at least {required_support} relevant independent source(s)")
        if verdict == "unclear":
            missing_evidence.append("resolve conflicting evidence with primary or higher-quality sources")

        return {
            "tool": "verify_claim",
            "claim": claim,
            "strictness": strict,
            "verdict": verdict,
            "confidence": confidence,
            "evidence": evidence,
            "missing_evidence": missing_evidence,
            "source_count": len(sources),
            "relevant_source_count": len(evidence),
        }
    except Exception as exc:
        return err("verify_claim", exc)
