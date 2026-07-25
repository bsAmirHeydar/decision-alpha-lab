from __future__ import annotations

import hashlib
from pathlib import Path


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def verify_hash_ledger(repo_root: Path, ledger_path: Path) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for line in ledger_path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            expected, relative = line.split("  ", 1)
        except ValueError:
            errors.append("LEDGER_FORMAT:" + line)
            continue
        relative = relative.strip().replace("\\", "/")
        if relative in seen:
            errors.append("LEDGER_DUPLICATE:" + relative)
            continue
        seen.add(relative)
        path = repo_root / relative
        if not path.is_file():
            errors.append("LEDGER_MISSING:" + relative)
        elif _digest(path) != expected:
            errors.append("LEDGER_HASH:" + relative)
    if not seen:
        errors.append("LEDGER_EMPTY")
    return errors
