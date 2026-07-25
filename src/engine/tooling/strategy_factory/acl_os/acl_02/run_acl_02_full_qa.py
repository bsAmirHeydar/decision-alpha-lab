from __future__ import annotations
import json,subprocess,sys
from ..common import REPO_ROOT,dump_json
from .validate_acl_02 import validate

def main()->int:
 p=subprocess.run([sys.executable,"-m","pytest","-q","src/engine/legacy/acl_os_reference/tests_acl_02"],cwd=REPO_ROOT,text=True,capture_output=True)
 v=validate(REPO_ROOT);out={"passed":p.returncode==0 and v["passed"],"pytest":{"returncode":p.returncode,"stdout":p.stdout[-20000:],"stderr":p.stderr[-8000:]},"validation":v,"claim_ceiling":"SEMANTIC_INTAKE_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
 dump_json(REPO_ROOT/"releases/history/acl_os/reports/ACL_OS_02_QA_REPORT.json",out);print(json.dumps(out,indent=2,sort_keys=True));return 0 if out["passed"] else 1
if __name__=="__main__":raise SystemExit(main())
