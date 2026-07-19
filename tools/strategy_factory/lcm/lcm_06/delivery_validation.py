def validate(repo_root):
    required = [
        "README_ALPHA_LAB_LCM_06.md",
        "INSTALL_ALPHA_LAB_LCM_06.md",
        "COMMIT_MESSAGE_LCM_06.md",
        "LCM_06_FILE_INDEX.txt",
        "LCM_06_ARTIFACT_INVENTORY.csv",
        "LCM_06_FILE_HASHES.sha256",
        "LCM_06_PATCH_MANIFEST.json",
        "LCM_06_QA_REPORT.json",
    ]
    missing = [x for x in required if not (repo_root / x).is_file()]
    return {"passed": not missing, "missing": missing}
