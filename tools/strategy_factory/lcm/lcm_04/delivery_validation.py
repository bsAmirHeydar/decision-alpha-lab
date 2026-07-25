from pathlib import Path

def validate(repo_root: Path):
    required=['releases/history/lcm/readmes/README_ALPHA_LAB_LCM_04.md','releases/history/lcm/installers/INSTALL_ALPHA_LAB_LCM_04.md','releases/history/lcm/commit_messages/COMMIT_MESSAGE_LCM_04.md','releases/history/lcm/indexes/LCM_04_FILE_INDEX.txt','releases/history/lcm/inventories/LCM_04_ARTIFACT_INVENTORY.csv','releases/history/lcm/hashes/LCM_04_FILE_HASHES.sha256']
    missing=[x for x in required if not (repo_root/x).is_file()]
    return {'passed':not missing,'missing':missing}
