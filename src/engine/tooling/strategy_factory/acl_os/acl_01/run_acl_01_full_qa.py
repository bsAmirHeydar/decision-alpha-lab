from __future__ import annotations
import json,subprocess,sys
from ..common import REPO_ROOT,dump_json
from .validate_acl_01 import validate

def main()->int:
    proc=subprocess.run([sys.executable,"-m","pytest","-q","src/engine/legacy/acl_os_reference/tests_acl_01"],cwd=REPO_ROOT,text=True,capture_output=True)
    validation=validate(REPO_ROOT)
    out={"passed":proc.returncode==0 and validation["passed"],"pytest":{"returncode":proc.returncode,"stdout":proc.stdout[-16000:],"stderr":proc.stderr[-5000:]},"validation":validation,"claim_ceiling":"REFERENCE_REPOSITORY_CONTROL_PLANE","live_order_submission_allowed":False,"capital_activation_allowed":False}
    dump_json(REPO_ROOT/"releases/history/acl_os/reports/ACL_OS_01_QA_REPORT.json",out); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
