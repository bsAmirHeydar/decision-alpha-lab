from __future__ import annotations

from pathlib import Path

from .canonical import file_digest


def verify_hash_ledger(repo_root: Path, ledger: Path) -> list[str]:
    errors: list[str] = []
    for line in ledger.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        path = repo_root / relative.strip()
        if not path.is_file():
            errors.append(f"MISSING:{relative.strip()}")
        elif file_digest(path) != expected:
            errors.append(f"HASH:{relative.strip()}")
    return errors
