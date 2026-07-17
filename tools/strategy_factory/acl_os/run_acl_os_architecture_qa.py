from __future__ import annotations
import json, subprocess, sys
from .common import REPO_ROOT, TEMPLATE_ROOT, dump_json
from .validate_acl_os_architecture import validate
from .validate_context_package import validate_context

def main() -> int:
    architecture=validate(REPO_ROOT)
    template=validate_context(TEMPLATE_ROOT,allow_placeholders=True)
    test_path=REPO_ROOT/"lab"/"11_strategy_factory"/"acl_os"/"tests"/"test_architecture_tools.py"
    proc=subprocess.run([sys.executable,"-m","pytest","-q",str(test_path)],cwd=REPO_ROOT,text=True,capture_output=True)
    report={
      "phase":"ACL_OS_ARCHITECTURE","version":"1.0.0","architecture":architecture,"context_template":template,
      "pytest":{"passed":proc.returncode==0,"stdout":proc.stdout[-12000:],"stderr":proc.stderr[-12000:]},
      "production_authorized":False,"capital_activation_allowed":False,
      "claim_ceiling":"REFERENCE_ARCHITECTURE_ONLY"
    }
    report["passed"]=architecture["passed"] and template["passed"] and proc.returncode==0
    report["status"]="passed_reference_architecture_qa" if report["passed"] else "failed"
    dump_json(REPO_ROOT/"ACL_OS_ARCHITECTURE_QA_REPORT.json",report)
    print(json.dumps(report,indent=2,sort_keys=True)); return 0 if report["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
