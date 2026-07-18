from __future__ import annotations
from pathlib import Path

def validate_delivery(repo_root: Path) -> dict:
    required=[
      'README_ALPHA_LAB_LCM_01.md','INSTALL_ALPHA_LAB_LCM_01.md','COMMIT_MESSAGE_LCM_01.md',
      'LCM_01_FILE_INDEX.txt','LCM_01_FILE_HASHES.sha256','LCM_01_ARTIFACT_INVENTORY.csv',
      'LCM_01_PATCH_MANIFEST.json','LCM_01_QA_REPORT.json',
      'docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/11_PHASE_DELIVERIES/LCM_01/00_MOC.md',
      'docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/12_ATOMIC_CONCEPTS/LCM_01/00_MOC.md',
    ]
    missing=[x for x in required if not (repo_root/x).is_file()]
    return {'passed':not missing,'required_count':len(required),'missing':missing}
