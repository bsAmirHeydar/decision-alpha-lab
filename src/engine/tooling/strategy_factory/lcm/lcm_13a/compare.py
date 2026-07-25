from __future__ import annotations
from typing import Any
from .constants import HARD_DIMENSIONS

FIELD_BY_DIMENSION = {
    "INPUT_DIGEST": "input_digest",
    "KNOWN_TIME": "known_time",
    "STATE": "state",
    "EVENT": "event",
    "DECISION": "decision",
    "REQUEST": "request",
    "VISUAL_ANCHOR": "visual_anchor",
    "REASON_CODE": "reason_codes",
    "RESOLVED_LOCATOR": "resolved_locator",
    "SIDE_EFFECT_AUTHORITY": "side_effect_authority",
}

class DualRunComparator:
    def compare(self, *, input_digest: str, legacy: dict[str, Any], canonical: dict[str, Any], domain: str) -> list[dict[str, Any]]:
        legacy_view = dict(legacy)
        canonical_view = dict(canonical)
        legacy_view["input_digest"] = input_digest
        canonical_view["input_digest"] = input_digest
        results: list[dict[str, Any]] = []
        canonical_blocked = canonical.get("availability") == "BLOCKED"
        for dimension in HARD_DIMENSIONS:
            field = FIELD_BY_DIMENSION[dimension]
            if dimension == "VISUAL_ANCHOR" and domain != "VISUAL":
                status = "NOT_APPLICABLE"
            elif canonical_blocked and dimension not in {"INPUT_DIGEST", "SIDE_EFFECT_AUTHORITY"}:
                status = "BLOCKED_NOT_COMPARABLE"
            else:
                status = "PASS" if legacy_view.get(field) == canonical_view.get(field) else "MISMATCH"
            results.append({
                "dimension": dimension,
                "field": field,
                "legacy_value": legacy_view.get(field),
                "canonical_value": canonical_view.get(field),
                "status": status,
                "tolerance_applied": False,
            })
        return results
