from __future__ import annotations
from pathlib import Path
REQUIRED=[
 'src/engine/tooling/strategy_factory/acl_os/acl_09/service.py','registry/history/acl/acl_09/registry_manifest.json','src/engine/legacy/acl_os_reference/tests_acl_09/conftest.py','src/engine/legacy/acl_os_reference/fixtures/acl_09/reference_memory/memory_receipt.json','mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL09/ACL09.mqh','docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_09/00_MOC.md','docs/architecture/master/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_09/000_MOC.md']
def validate_delivery(repo_root:Path)->dict:
    missing=[x for x in REQUIRED if not (repo_root/x).is_file()]
    return {'passed':not missing,'missing':missing,'required_count':len(REQUIRED)}
