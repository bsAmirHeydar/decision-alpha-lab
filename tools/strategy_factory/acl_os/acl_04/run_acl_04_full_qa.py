from __future__ import annotations
import json
import os
import subprocess
import sys
from ..common import REPO_ROOT, dump_json
from .validate_acl_04 import validate


def main() -> int:
    env={**os.environ,"PYTEST_DISABLE_PLUGIN_AUTOLOAD":"1"}
    proc=subprocess.run([sys.executable,"-m","pytest","-q","lab/11_strategy_factory/acl_os/tests_acl_04"],cwd=REPO_ROOT,text=True,capture_output=True,env=env)
    validation=validate(REPO_ROOT)
    out={"passed":proc.returncode==0 and validation["passed"],"pytest":{"returncode":proc.returncode,"stdout":proc.stdout[-30000:],"stderr":proc.stderr[-10000:]},"validation":validation,"claim_ceiling":"SETUP_DEFINITION_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
    dump_json(REPO_ROOT/"ACL_OS_04_QA_REPORT.json",out); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out["passed"] else 1

if __name__=="__main__": raise SystemExit(main())
