from __future__ import annotations
from pathlib import Path

def validate(repo_root: Path):
    required=['releases/history/lcm/indexes/LCM_02_FILE_INDEX.txt','releases/history/lcm/hashes/LCM_02_FILE_HASHES.sha256','releases/history/lcm/inventories/LCM_02_ARTIFACT_INVENTORY.csv','releases/history/lcm/manifests/LCM_02_PATCH_MANIFEST.json','releases/history/lcm/reports/LCM_02_QA_REPORT.json','releases/history/lcm/commit_messages/COMMIT_MESSAGE_LCM_02.md','releases/history/lcm/installers/INSTALL_ALPHA_LAB_LCM_02.md']
    missing=[x for x in required if not (repo_root/x).is_file()]
    return {'passed':not missing,'missing':missing}
