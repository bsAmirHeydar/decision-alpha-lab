from __future__ import annotations
from pathlib import Path
REQUIRED=[
 'tools/strategy_factory/acl_os/acl_09/service.py','registry/acl_os/acl_09/registry_manifest.json','lab/11_strategy_factory/acl_os/tests_acl_09/conftest.py','lab/11_strategy_factory/acl_os/fixtures/acl_09/reference_memory/memory_receipt.json','lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/ACL09/ACL09.mqh','docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_09/00_MOC.md','docs/alpha_lab_master_architecture/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_09/000_MOC.md']
def validate_delivery(repo_root:Path)->dict:
    missing=[x for x in REQUIRED if not (repo_root/x).is_file()]
    return {'passed':not missing,'missing':missing,'required_count':len(REQUIRED)}
