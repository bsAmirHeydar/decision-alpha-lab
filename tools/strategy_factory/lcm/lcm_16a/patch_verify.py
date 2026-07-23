from __future__ import annotations

from pathlib import Path

from .io import file_digest


def verify_hash_ledger(repo_root: Path, ledger_path: Path) -> int:
    count = 0
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        path = repo_root / relative
        if not path.is_file() or file_digest(path) != digest:
            raise ValueError(f"hash ledger mismatch: {relative}")
        count += 1
    return count
