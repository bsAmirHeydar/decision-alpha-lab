from __future__ import annotations
import json
from .policies import REPO_ROOT
REQUIRED=['src/engine/tooling/strategy_factory/acl_os/acl_06/service.py','registry/history/acl/acl_06/schemas/v1/research_dag.schema.json','registry/history/acl/acl_06/policies/v1/dag_execution_policy.json','src/engine/legacy/acl_os_reference/tests_acl_06/test_service.py','src/engine/legacy/acl_os_reference/fixtures/acl_06/reference_run/execution/research_run.json','docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_06/00_MOC.md','docs/architecture/master/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_06/00_MOC.md']
def run():
    missing=[p for p in REQUIRED if not (REPO_ROOT/p).is_file()]; result={'phase':'ACL-06','required_count':len(REQUIRED),'missing':missing,'passed':not missing}; print(json.dumps(result,indent=2,sort_keys=True)); return result
if __name__=='__main__': raise SystemExit(0 if run()['passed'] else 2)
