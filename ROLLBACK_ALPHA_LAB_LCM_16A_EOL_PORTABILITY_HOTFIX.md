# Rollback — LCM-16A EOL Portability Hotfix

Before commit, restore only paths listed in `LCM_16A_EOL_HOTFIX_FILE_INDEX.txt` from Git and remove only newly added hotfix paths. Do not use wildcard deletion.

After commit, use `git revert <hotfix-commit>` rather than rewriting shared history. The original LCM-16A patch receipt remains historical evidence and is not rewritten by this hotfix.
