from __future__ import annotations
import json,subprocess,sys
from ..common import REPO_ROOT,dump_json
from .validate_acl_03 import validate

def main()->int:
    p=subprocess.run([sys.executable,"-m","pytest","-q","lab/11_strategy_factory/acl_os/tests_acl_03"],cwd=REPO_ROOT,text=True,capture_output=True)
    v=validate(REPO_ROOT)
    out={"passed":p.returncode==0 and v["passed"],"pytest":{"returncode":p.returncode,"stdout":p.stdout[-30000:],"stderr":p.stderr[-10000:]},"validation":v,"claim_ceiling":"CONTEXT_COMPILATION_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
    dump_json(REPO_ROOT/"ACL_OS_03_QA_REPORT.json",out);print(json.dumps(out,indent=2,sort_keys=True));return 0 if out["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
