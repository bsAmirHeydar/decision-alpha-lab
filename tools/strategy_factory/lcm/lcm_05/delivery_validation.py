def validate(repo_root):
    required=['README_ALPHA_LAB_LCM_05.md','INSTALL_ALPHA_LAB_LCM_05.md','COMMIT_MESSAGE_LCM_05.md','LCM_05_FILE_INDEX.txt'];missing=[x for x in required if not (repo_root/x).is_file()];return {"passed":not missing,"missing":missing}
