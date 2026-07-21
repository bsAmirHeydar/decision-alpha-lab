from __future__ import annotations
from pathlib import Path

def protected_paths(repo_root: Path) -> set[str]:
    protected: set[str] = set()
    for ledger in sorted(repo_root.rglob("*_FILE_HASHES.sha256")):
        if "LCM_12B" in ledger.name:
            continue
        for line in ledger.read_text(encoding="utf-8", errors="ignore").splitlines():
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                protected.add(parts[1].lstrip("*").strip().replace("\\", "/"))
    return protected
