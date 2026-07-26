from __future__ import annotations
from pathlib import Path
def validate_delivery(root: Path) -> dict:
    required=['src/engine/tooling/strategy_factory/acl_os/acl_11/service.py','registry/history/acl/acl_11/schemas/v1/runtime_custody_decision.schema.json','src/engine/legacy/acl_os_reference/tests_acl_11/test_service.py','docs/architecture/master/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_11_RUNTIME_PARITY_AND_HANDOFF.md','docs/architecture/master/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_12_SECURITY_HARDENING.md']
    missing=[p for p in required if not (root/p).is_file()]
    return {'passed':not missing,'missing':missing}
