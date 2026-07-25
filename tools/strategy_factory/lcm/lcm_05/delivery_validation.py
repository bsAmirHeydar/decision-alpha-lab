def validate(repo_root):
    required=['releases/history/lcm/readmes/README_ALPHA_LAB_LCM_05.md','releases/history/lcm/installers/INSTALL_ALPHA_LAB_LCM_05.md','releases/history/lcm/commit_messages/COMMIT_MESSAGE_LCM_05.md','releases/history/lcm/indexes/LCM_05_FILE_INDEX.txt'];missing=[x for x in required if not (repo_root/x).is_file()];return {"passed":not missing,"missing":missing}
