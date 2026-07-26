from __future__ import annotations
from pathlib import Path
def validate_delivery(root:Path)->dict:
    required=['releases/history/acl_os/readmes/README_ALPHA_LAB_ACL_OS_15.md','releases/history/acl_os/installers/INSTALL_ALPHA_LAB_ACL_OS_15.md','COMMIT_MESSAGE.md','COMMIT_MESSAGE.txt','src/engine/tooling/strategy_factory/acl_os/acl_15/service.py','registry/history/acl/acl_15/schemas/v1/fleet_registration_contract.schema.json','src/engine/legacy/acl_os_reference/tests_acl_15/test_service.py','docs/architecture/master/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_15_FLEET_OPERATIONS_AND_CLOSURE.md']
    missing=[x for x in required if not (root/x).is_file()]
    return {'passed':not missing,'missing':missing,'required_count':len(required)}
