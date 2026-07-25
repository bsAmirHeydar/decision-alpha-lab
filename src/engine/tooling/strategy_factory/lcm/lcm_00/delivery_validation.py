from __future__ import annotations

from pathlib import Path

from .canonical import sha256_file


def validate_patch_boundary(source_root: Path, work_root: Path, patch_paths: list[str]) -> dict:
    source_paths = {p.relative_to(source_root).as_posix() for p in source_root.rglob("*") if p.is_file()}
    work_paths = {p.relative_to(work_root).as_posix() for p in work_root.rglob("*") if p.is_file()}
    deleted = sorted(source_paths - work_paths)
    changed = []
    for rel in sorted(source_paths & work_paths):
        if sha256_file(source_root / rel) != sha256_file(work_root / rel):
            changed.append(rel)
    declared = set(patch_paths)
    actual_delta = set(changed) | (work_paths - source_paths)
    return {
        "passed": not deleted and actual_delta == declared,
        "deleted_paths": deleted,
        "changed_or_added_count": len(actual_delta),
        "undeclared_delta": sorted(actual_delta - declared),
        "declared_but_unchanged": sorted(declared - actual_delta),
    }
