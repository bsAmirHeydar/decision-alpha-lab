from __future__ import annotations
from pathlib import Path
from .canonical import file_digest
def verify_patch(repo_root:Path,ledger:Path)->dict:
    errors=[];count=0
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if not line.strip():continue
        expected,path=line.split("  ",1);p=repo_root/path;count+=1
        if not p.is_file():errors.append({"path":path,"code":"MISSING"})
        elif file_digest(p)!=expected:errors.append({"path":path,"code":"HASH_MISMATCH"})
    return {"passed":not errors,"checked":count,"errors":errors}
