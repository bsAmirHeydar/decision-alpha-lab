"""Semantic diff for two FP-I00 baseline manifests."""
from __future__ import annotations

from typing import Any


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(value, dict):
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else str(key)
            out.update(_flatten(value[key], child))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            out.update(_flatten(item, f"{prefix}[{index}]"))
    else:
        out[prefix] = value
    return out


def semantic_diff(left: dict, right: dict, ignored_paths: tuple[str, ...] = ()) -> list[dict]:
    left_flat = _flatten(left)
    right_flat = _flatten(right)
    keys = sorted(set(left_flat) | set(right_flat))
    changes = []
    for key in keys:
        if any(key == ignored or key.startswith(ignored + ".") for ignored in ignored_paths):
            continue
        before = left_flat.get(key, "<MISSING>")
        after = right_flat.get(key, "<MISSING>")
        if before != after:
            changes.append({"path": key, "before": before, "after": after})
    return changes
