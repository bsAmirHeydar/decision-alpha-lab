"""Snapshot and comparison utilities for the additive UCEE boundary."""
from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Iterable

from .canonical import content_hash, file_hash
from .enums import DecisionStatus, ReasonCode


DEFAULT_CORE_PATTERNS = (
    "src/engine/packages/strategy_factory_*/**",
    "schemas/legacy/strategy_factory/v*/**",
    "mql5/Include/AlphaLab/StrategyFactory/**",
    "mql5/Experts/StrategyFactory/**",
)


def capture_snapshot(root: str | Path, patterns: Iterable[str] = DEFAULT_CORE_PATTERNS, exclude: Iterable[str] = ()) -> dict:
    root = Path(root)
    exclusions = tuple(exclude)
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if any(fnmatch.fnmatch(rel, x) for x in exclusions):
            continue
        if any(fnmatch.fnmatch(rel, p) for p in patterns):
            files[rel] = file_hash(path)
    return {
        "patterns": list(patterns),
        "files": files,
        "snapshot_hash": content_hash(files),
    }


def compare_snapshots(before: dict, after: dict) -> dict:
    b = before.get("files", {})
    a = after.get("files", {})
    added = sorted(set(a) - set(b))
    removed = sorted(set(b) - set(a))
    modified = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    changed = bool(added or removed or modified)
    return {
        "status": DecisionStatus.REJECT.value if changed else DecisionStatus.ALLOW.value,
        "reason_codes": [ReasonCode.CORE_BOUNDARY_CHANGED.value] if changed else [ReasonCode.OK.value],
        "added": added,
        "removed": removed,
        "modified": modified,
        "before_hash": before.get("snapshot_hash"),
        "after_hash": after.get("snapshot_hash"),
    }
