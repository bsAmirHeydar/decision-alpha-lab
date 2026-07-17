from __future__ import annotations
import hashlib,json
from ..common import REPO_ROOT

def main()->int:
 index=REPO_ROOT/"ACL_OS_02_FILE_INDEX.txt";ledger=REPO_ROOT/"ACL_OS_02_FILE_HASHES.sha256";errors=[];files=[]
 if not index.is_file() or not ledger.is_file():errors.append("missing index or hash ledger")
 else:
  files=[x.strip() for x in index.read_text(encoding="utf-8").splitlines() if x.strip()]
  entries={line.split("  ",1)[1]:line.split("  ",1)[0] for line in ledger.read_text(encoding="utf-8").splitlines() if "  " in line}
  for rel in files:
   p=REPO_ROOT/rel
   if not p.is_file():errors.append(f"missing {rel}");continue
   if rel in {"ACL_OS_02_FILE_HASHES.sha256","ACL_OS_02_ARTIFACT_INVENTORY.csv","ACL_OS_02_QA_REPORT.json"}:continue
   got=hashlib.sha256(p.read_bytes()).hexdigest();exp=entries.get(rel)
   if exp!=got:errors.append(f"hash mismatch {rel}")
 out={"passed":not errors,"errors":errors,"indexed_files":len(files)};print(json.dumps(out,indent=2,sort_keys=True));return 0 if out["passed"] else 1
if __name__=="__main__":raise SystemExit(main())
