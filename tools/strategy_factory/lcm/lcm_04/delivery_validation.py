from pathlib import Path

def validate(repo_root: Path):
    required=['README_ALPHA_LAB_LCM_04.md','INSTALL_ALPHA_LAB_LCM_04.md','COMMIT_MESSAGE_LCM_04.md','LCM_04_FILE_INDEX.txt','LCM_04_ARTIFACT_INVENTORY.csv','LCM_04_FILE_HASHES.sha256']
    missing=[x for x in required if not (repo_root/x).is_file()]
    return {'passed':not missing,'missing':missing}
