from __future__ import annotations
from pathlib import Path
def validate_delivery(root: Path) -> dict:
    required=['tools/strategy_factory/acl_os/acl_11/service.py','registry/acl_os/acl_11/schemas/v1/runtime_custody_decision.schema.json','lab/11_strategy_factory/acl_os/tests_acl_11/test_service.py','docs/alpha_lab_master_architecture/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_11_RUNTIME_PARITY_AND_HANDOFF.md','docs/alpha_lab_master_architecture/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_12_SECURITY_HARDENING.md']
    missing=[p for p in required if not (root/p).is_file()]
    return {'passed':not missing,'missing':missing}
