from __future__ import annotations
import hashlib
import json
from ..common import REPO_ROOT


def main() -> int:
    index=REPO_ROOT/"ACL_OS_04_FILE_INDEX.txt"; ledger=REPO_ROOT/"ACL_OS_04_FILE_HASHES.sha256"; errors=[]; files=[]
    if not index.is_file() or not ledger.is_file(): errors.append("missing index or hash ledger")
    else:
        files=[x.strip() for x in index.read_text(encoding="utf-8").splitlines() if x.strip()]
        entries={line.split("  ",1)[1]:line.split("  ",1)[0] for line in ledger.read_text(encoding="utf-8").splitlines() if "  " in line}
        skip={"ACL_OS_04_FILE_HASHES.sha256","ACL_OS_04_ARTIFACT_INVENTORY.csv","ACL_OS_04_QA_REPORT.json"}
        for rel in files:
            path=REPO_ROOT/rel
            if not path.is_file(): errors.append(f"missing {rel}"); continue
            if rel in skip: continue
            got=hashlib.sha256(path.read_bytes()).hexdigest(); expected=entries.get(rel)
            if got != expected: errors.append(f"hash mismatch {rel}")
    out={"passed":not errors,"errors":errors,"indexed_files":len(files)}; print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out["passed"] else 1

if __name__=="__main__": raise SystemExit(main())
