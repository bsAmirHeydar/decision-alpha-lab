from __future__ import annotations
from pathlib import Path
from .replay_validator import verify_generated_root
from .static_validator import validate_registry_files
def validate_delivery(repo_root:Path)->dict:
    root=repo_root/'src/engine/legacy/acl_os_reference/fixtures/acl_08/reference_report'; a=verify_generated_root(root); b=validate_registry_files()
    required=[repo_root/'src/engine/tooling/strategy_factory/acl_os/acl_08',repo_root/'registry/acl_os/acl_08',repo_root/'docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_08',repo_root/'docs/alpha_lab_master_architecture/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_08']
    checks={'reference_root':a['passed'],'registry':b['passed'],'required_paths':all(x.exists() for x in required)}
    return {'passed':all(checks.values()),'checks':checks,'schema_count':b['schema_count'],'policy_count':b['policy_count']}
