def validate(repo_root):
    required = [
        "releases/history/lcm/readmes/README_ALPHA_LAB_LCM_06.md",
        "releases/history/lcm/installers/INSTALL_ALPHA_LAB_LCM_06.md",
        "releases/history/lcm/commit_messages/COMMIT_MESSAGE_LCM_06.md",
        "releases/history/lcm/indexes/LCM_06_FILE_INDEX.txt",
        "releases/history/lcm/inventories/LCM_06_ARTIFACT_INVENTORY.csv",
        "releases/history/lcm/hashes/LCM_06_FILE_HASHES.sha256",
        "releases/history/lcm/manifests/LCM_06_PATCH_MANIFEST.json",
        "releases/history/lcm/reports/LCM_06_QA_REPORT.json",
    ]
    missing = [x for x in required if not (repo_root / x).is_file()]
    return {"passed": not missing, "missing": missing}
