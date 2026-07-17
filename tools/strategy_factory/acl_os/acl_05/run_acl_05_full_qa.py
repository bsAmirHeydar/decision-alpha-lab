from __future__ import annotations
import json, os, subprocess, sys
from .policies import REPO_ROOT
from .replay import verify_frozen_batch
from .validate_acl_05 import run as static_run
from .validate_acl_05_delivery import run as delivery_run

def _command(name,args):
    env=os.environ.copy()
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"]="1"
    try:
        proc=subprocess.run(args,cwd=REPO_ROOT,text=True,capture_output=True,timeout=180,env=env)
        return {"name":name,"passed":proc.returncode==0,"return_code":proc.returncode,"stdout":proc.stdout[-8000:],"stderr":proc.stderr[-8000:]}
    except subprocess.TimeoutExpired as exc:
        return {"name":name,"passed":False,"return_code":124,"stdout":(exc.stdout or "")[-8000:] if isinstance(exc.stdout,str) else "","stderr":"ACL05_QA_COMMAND_TIMEOUT"}

def run() -> dict:
    static=static_run(); delivery=delivery_run()
    commands=[
      _command("acl05_pytest",[sys.executable,"-m","pytest","-q","lab/11_strategy_factory/acl_os/tests_acl_05"]),
      _command("acl04_regression",[sys.executable,"-m","pytest","-q","lab/11_strategy_factory/acl_os/tests_acl_04"]),
      _command("acl05_compileall",[sys.executable,"-m","compileall","-q","tools/strategy_factory/acl_os/acl_05"]),
    ]
    replay=verify_frozen_batch(REPO_ROOT/"lab/11_strategy_factory/acl_os/fixtures/acl_05/reference_batch")
    result={"phase":"ACL-05","claim_ceiling":"RESEARCH_BATCH_FREEZE_REFERENCE_ONLY","static":static,"delivery":delivery,"commands":commands,"reference_replay":replay,"metaeditor_compile_performed":False,"mt5_runtime_parity_claimed":False,"production_authorization_claimed":False}
    result["passed"]=static["passed"] and delivery["passed"] and all(c["passed"] for c in commands) and replay["passed"]
    out=REPO_ROOT/"ACL_OS_05_QA_REPORT.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    return result
if __name__=="__main__":
    raise SystemExit(0 if run()["passed"] else 2)
