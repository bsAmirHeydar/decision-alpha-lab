from __future__ import annotations
from pathlib import Path
from .canonical import file_digest

def verify_hash_ledger(repo_root:Path,ledger_path:Path):
    errors=[]
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():continue
        expected,rel=line.split(None,1);rel=rel.strip().lstrip("*")
        path=repo_root/rel
        if not path.is_file():errors.append(f"MISSING:{rel}");continue
        if file_digest(path)!=expected:errors.append(f"HASH:{rel}")
    return errors
