from __future__ import annotations

from .canonical import digest_object
from .registries import HARD_DIMENSIONS, SOFT_DIMENSIONS
from .trace_normalizer import normalize_trace


def compare(legacy, canonical, soft_tolerances=None):
    soft_tolerances = soft_tolerances or {
        "latency_us": 1000,
        "memory_bytes": 4096,
        "visual_width": 0,
        "visual_color": 0,
    }
    left, right = normalize_trace(legacy), normalize_trace(canonical)
    hard: list[dict] = []
    soft: list[dict] = []
    unknown: list[dict] = []

    if left["event_count"] != right["event_count"]:
        hard.append({"dimension": "event_count", "legacy": left["event_count"], "canonical": right["event_count"]})

    for index, (legacy_event, canonical_event) in enumerate(zip(left["events"], right["events"])):
        for dimension in HARD_DIMENSIONS:
            legacy_value = legacy_event.get(dimension)
            canonical_value = canonical_event.get(dimension)
            legacy_missing = dimension in legacy_event.get("missing_hard_dimensions", [])
            canonical_missing = dimension in canonical_event.get("missing_hard_dimensions", [])
            if legacy_missing and canonical_missing:
                unknown.append({"event_index": index, "dimension": dimension, "reason_code": "TRACE_EVIDENCE_UNKNOWN"})
            elif legacy_missing != canonical_missing or legacy_value != canonical_value:
                hard.append({"event_index": index, "dimension": dimension, "legacy": legacy_value, "canonical": canonical_value})
        for dimension in SOFT_DIMENSIONS:
            legacy_value = legacy_event.get(dimension)
            canonical_value = canonical_event.get(dimension)
            if legacy_value is None and canonical_value is None:
                continue
            if isinstance(legacy_value, (int, float)) and isinstance(canonical_value, (int, float)):
                if abs(legacy_value - canonical_value) > soft_tolerances.get(dimension, 0):
                    soft.append({"event_index": index, "dimension": dimension, "legacy": legacy_value, "canonical": canonical_value})
            elif legacy_value != canonical_value:
                soft.append({"event_index": index, "dimension": dimension, "legacy": legacy_value, "canonical": canonical_value})

    if hard:
        status, reason = "HARD_MISMATCH", "TRACE_HARD_MISMATCH"
    elif unknown:
        status, reason = "UNKNOWN_EVIDENCE", "TRACE_EVIDENCE_UNKNOWN"
    elif soft:
        status, reason = "SOFT_MISMATCH", "TRACE_SOFT_MISMATCH"
    else:
        status, reason = "PASS", "TRACE_HARD_PARITY"

    out = {
        "schema_version": "1.0.0",
        "legacy_trace_id": legacy.get("trace_id"),
        "canonical_trace_id": canonical.get("trace_id"),
        "comparison_status": status,
        "reason_code": reason,
        "hard_mismatch_count": len(hard),
        "soft_mismatch_count": len(soft),
        "unknown_evidence_count": len(unknown),
        "hard_mismatches": hard,
        "soft_mismatches": soft,
        "unknown_evidence": unknown,
        "hard_mismatch_waived": False,
        "comparison_digest": None,
    }
    out["comparison_digest"] = digest_object(out, "comparison_digest")
    return out
