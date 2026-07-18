from __future__ import annotations
import json
from .policies import REPO_ROOT
REQUIRED=['tools/strategy_factory/acl_os/acl_06/service.py','registry/acl_os/acl_06/schemas/v1/research_dag.schema.json','registry/acl_os/acl_06/policies/v1/dag_execution_policy.json','lab/11_strategy_factory/acl_os/tests_acl_06/test_service.py','lab/11_strategy_factory/acl_os/fixtures/acl_06/reference_run/execution/research_run.json','docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_06/00_MOC.md','docs/alpha_lab_master_architecture/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_06/00_MOC.md']
def run():
    missing=[p for p in REQUIRED if not (REPO_ROOT/p).is_file()]; result={'phase':'ACL-06','required_count':len(REQUIRED),'missing':missing,'passed':not missing}; print(json.dumps(result,indent=2,sort_keys=True)); return result
if __name__=='__main__': raise SystemExit(0 if run()['passed'] else 2)
