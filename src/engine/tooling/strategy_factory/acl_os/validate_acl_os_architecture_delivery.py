from __future__ import annotations
import hashlib, json
from pathlib import Path
from .common import REPO_ROOT

def validate(repo: Path=REPO_ROOT) -> dict:
    errors=[]; index=repo/"releases/history/acl_os/indexes/ACL_OS_ARCHITECTURE_FILE_INDEX.txt"; ledger=repo/"releases/history/acl_os/hashes/ACL_OS_ARCHITECTURE_FILE_HASHES.sha256"
    if not index.is_file(): errors.append("missing file index")
    else:
        for rel in index.read_text(encoding="utf-8").splitlines():
            if rel and not (repo/rel).is_file(): errors.append(f"missing indexed file: {rel}")
    if not ledger.is_file(): errors.append("missing hash ledger")
    else:
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            digest,rel=line.split("  ",1); p=repo/rel
            if not p.is_file(): errors.append(f"missing hashed file: {rel}"); continue
            actual=hashlib.sha256(p.read_bytes()).hexdigest()
            if actual!=digest: errors.append(f"hash mismatch: {rel}")
    return {"passed":not errors,"errors":errors}

def main() -> int:
    out=validate(); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
