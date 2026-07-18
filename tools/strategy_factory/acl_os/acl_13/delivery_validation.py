from __future__ import annotations
from pathlib import Path
def validate_delivery(root:Path)->dict:
    required=['tools/strategy_factory/acl_os/acl_13/service.py','registry/acl_os/acl_13/schemas/v1/one_hour_assessment_result.schema.json','lab/11_strategy_factory/acl_os/tests_acl_13/test_service.py','docs/alpha_lab_master_architecture/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_13_ONE_HOUR_ASSESSMENT_PRODUCT.md','docs/alpha_lab_master_architecture/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_14_FIRST_REAL_CONTEXT_PILOT.md']
    missing=[p for p in required if not (root/p).is_file()]
    return {'passed':not missing,'missing':missing}
