from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
from ..common import REPO_ROOT,dump_json
from .validate_acl_00 import validate

def main()->int:
    cmd=[sys.executable,"-m","pytest","-q","src/engine/legacy/acl_os_reference/tests_acl_00"]
    proc=subprocess.run(cmd,cwd=REPO_ROOT,text=True,capture_output=True)
    validation=validate(REPO_ROOT)
    out={"passed":proc.returncode==0 and validation["passed"],"pytest":{"returncode":proc.returncode,"stdout":proc.stdout[-12000:],"stderr":proc.stderr[-4000:]},"validation":validation,"claim_ceiling":"REFERENCE_CONTROL_PLANE","capital_activation_allowed":False,"live_order_submission_allowed":False}
    dump_json(REPO_ROOT/"releases/history/acl_os/reports/ACL_OS_00_QA_REPORT.json",out); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
