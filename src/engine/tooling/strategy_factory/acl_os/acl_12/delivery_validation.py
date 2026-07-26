from __future__ import annotations
from pathlib import Path
def validate_delivery(root:Path)->dict:
    required=['src/engine/tooling/strategy_factory/acl_os/acl_12/service.py','registry/history/acl/acl_12/schemas/v1/security_readiness_decision.schema.json','src/engine/legacy/acl_os_reference/tests_acl_12/test_service.py','docs/architecture/master/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_12_SECURITY_HARDENING.md','docs/architecture/master/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_13_ONE_HOUR_ASSESSMENT_PRODUCT.md']
    missing=[p for p in required if not (root/p).is_file()]
    return {'passed':not missing,'missing':missing}
