from __future__ import annotations

from pathlib import Path


def validate_file_index(repo_root: Path, index: Path):
    rows = [
        line.strip().replace("\\", "/")
        for line in index.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    missing = [row for row in rows if not (repo_root / row).is_file()]
    return {
        "indexed_file_count": len(rows),
        "unique_file_count": len(set(rows)),
        "missing": missing,
        "passed": len(rows) == len(set(rows)) and not missing,
    }
