from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,subprocess,sys
from pathlib import Path
from .delivery_validator import validate_delivery
from .replay_validator import verify_generated_root
from .static_validator import validate_registry_files
def run_qa(repo_root:Path)->dict:
    reference=repo_root/'src/engine/legacy/acl_os_reference/fixtures/acl_08/reference_report'; static=validate_registry_files(); replay=verify_generated_root(reference); delivery=validate_delivery(repo_root)
    proc=subprocess.run([sys.executable,'-m','compileall','-q',str(repo_root/'src/engine/tooling/strategy_factory/acl_os/acl_08')],capture_output=True,text=True)
    checks={'static_registry':static['passed'],'reference_replay':replay['passed'],'delivery':delivery['passed'],'python_compileall':proc.returncode==0}
    return {'passed':all(checks.values()),'checks':checks,'schema_count':static['schema_count'],'policy_count':static['policy_count'],'compile_stderr':proc.stderr}
def main()->int:
    repo=find_repository_root(__file__); report=run_qa(repo); print(json.dumps(report,indent=2,sort_keys=True)); return 0 if report['passed'] else 2
if __name__=='__main__': raise SystemExit(main())
