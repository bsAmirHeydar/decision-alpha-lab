from __future__ import annotations
from pathlib import Path
REQUIRED=[
 'src/engine/tooling/strategy_factory/acl_os/acl_10/service.py','registry/acl_os/acl_10/registry_manifest.json','src/engine/legacy/acl_os_reference/tests_acl_10/conftest.py','src/engine/legacy/acl_os_reference/fixtures/acl_10/reference_promotion/promotion_receipt.json','mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL10/ACL10.mqh','docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_10/00_MOC.md','docs/alpha_lab_master_architecture/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_10/000_MOC.md']
def validate_delivery(repo_root:Path) -> dict:
    missing=[x for x in REQUIRED if not (repo_root/x).is_file()]
    return {'passed':not missing,'missing':missing,'required_count':len(REQUIRED)}
