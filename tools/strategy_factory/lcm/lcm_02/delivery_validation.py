from __future__ import annotations
from pathlib import Path

def validate(repo_root: Path):
    required=['LCM_02_FILE_INDEX.txt','LCM_02_FILE_HASHES.sha256','LCM_02_ARTIFACT_INVENTORY.csv','LCM_02_PATCH_MANIFEST.json','LCM_02_QA_REPORT.json','COMMIT_MESSAGE_LCM_02.md','INSTALL_ALPHA_LAB_LCM_02.md']
    missing=[x for x in required if not (repo_root/x).is_file()]
    return {'passed':not missing,'missing':missing}
