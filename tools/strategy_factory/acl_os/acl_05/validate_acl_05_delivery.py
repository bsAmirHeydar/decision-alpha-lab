from __future__ import annotations
import json
from pathlib import Path
from .policies import REPO_ROOT

REQUIRED=[
 "tools/strategy_factory/acl_os/acl_05/service.py",
 "registry/acl_os/acl_05/schemas/v1/batch_definition.schema.json",
 "registry/acl_os/acl_05/policies/v1/batch_freeze_policy.json",
 "lab/11_strategy_factory/acl_os/tests_acl_05/test_acl05_service.py",
 "lab/11_strategy_factory/acl_os/fixtures/acl_05/reference_batch/batch/batch_definition.json",
 "docs/alpha_lab_master_architecture/context_lifecycle_os/05_RESEARCH_BATCH/00_MOC.md",
 "docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_05/00_MOC.md",
 "docs/alpha_lab_master_architecture/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_05/00_MOC.md",
]
def run() -> dict:
    missing=[x for x in REQUIRED if not (REPO_ROOT/x).is_file()]
    result={"phase":"ACL-05","required_count":len(REQUIRED),"missing":missing,"passed":not missing}
    print(json.dumps(result,indent=2,sort_keys=True)); return result
if __name__=="__main__": raise SystemExit(0 if run()["passed"] else 2)
