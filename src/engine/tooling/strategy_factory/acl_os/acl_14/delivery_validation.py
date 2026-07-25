from __future__ import annotations
from pathlib import Path
def validate_delivery(root:Path)->dict:
    required=['releases/history/acl_os/readmes/README_ALPHA_LAB_ACL_OS_14.md','releases/history/acl_os/installers/INSTALL_ALPHA_LAB_ACL_OS_14.md','COMMIT_MESSAGE.md','COMMIT_MESSAGE.txt','src/engine/tooling/strategy_factory/acl_os/acl_14/service.py','registry/acl_os/acl_14/schemas/v1/pilot_request.schema.json','src/engine/legacy/acl_os_reference/tests_acl_14/test_service.py','docs/alpha_lab_master_architecture/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_14_FIRST_REAL_CONTEXT_PILOT.md']
    missing=[x for x in required if not (root/x).is_file()]
    return {'passed':not missing,'missing':missing,'required_count':len(required)}
