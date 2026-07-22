from __future__ import annotations
from pathlib import Path
from .io import file_digest
def verify_hash_ledger(repo_root:Path,ledger_path:Path)->int:
    count=0
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        digest,rel=line.split("  ",1);p=repo_root/rel
        if not p.is_file() or file_digest(p)!=digest: raise ValueError(rel)
        count+=1
    return count
