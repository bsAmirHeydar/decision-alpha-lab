from __future__ import annotations
from typing import Any
from .canonical import content_hash


def semantic_diff(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    left_rows = {(r["source_row_id"], r["scenario_id"]): r for r in left.get("rows", [])}
    right_rows = {(r["source_row_id"], r["scenario_id"]): r for r in right.get("rows", [])}
    changed = []
    for key in sorted(set(left_rows) & set(right_rows)):
        left_semantic = {k: v for k, v in left_rows[key].items() if k not in {"twin_row_id", "twin_row_hash"}}
        right_semantic = {k: v for k, v in right_rows[key].items() if k not in {"twin_row_id", "twin_row_hash"}}
        left_hash = content_hash(left_semantic)
        right_hash = content_hash(right_semantic)
        if left_hash != right_hash:
            changed.append({"source_row_id": key[0], "scenario_id": key[1], "left_hash": left_hash, "right_hash": right_hash})
    return {
        "left_twin_hash": left.get("twin_hash"), "right_twin_hash": right.get("twin_hash"),
        "added_pairs": [list(k) for k in sorted(set(right_rows) - set(left_rows))],
        "removed_pairs": [list(k) for k in sorted(set(left_rows) - set(right_rows))],
        "changed_pairs": changed, "equivalent": left == right,
    }
