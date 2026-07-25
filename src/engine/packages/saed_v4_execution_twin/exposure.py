from __future__ import annotations
from .canonical import content_hash, stable_id


def build_exposure_ledger(source_rows: list[dict], scenarios: list, twin_rows: list[dict]) -> dict:
    expected = sorted((r["row_id"], s.scenario_id) for r in source_rows for s in scenarios)
    observed = sorted((r["source_row_id"], r["scenario_id"]) for r in twin_rows)
    missing = sorted(set(expected) - set(observed)); unexpected = sorted(set(observed) - set(expected))
    duplicates = sorted({x for x in observed if observed.count(x) > 1})
    status_counts: dict[str, int] = {}
    for row in twin_rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    payload = {
        "expected_pair_count": len(expected), "observed_pair_count": len(observed),
        "missing_pairs": [{"source_row_id": a, "scenario_id": b} for a,b in missing],
        "unexpected_pairs": [{"source_row_id": a, "scenario_id": b} for a,b in unexpected],
        "duplicate_pairs": [{"source_row_id": a, "scenario_id": b} for a,b in duplicates],
        "status_counts": dict(sorted(status_counts.items())), "complete": not missing and not unexpected and not duplicates and len(expected)==len(observed),
    }
    payload["ledger_id"] = stable_id("exectwinexposure", payload); payload["ledger_hash"] = content_hash(payload)
    return payload
