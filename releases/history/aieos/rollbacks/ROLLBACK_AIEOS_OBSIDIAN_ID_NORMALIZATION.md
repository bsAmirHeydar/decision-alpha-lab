# Rollback

Prefer `git revert <commit>` after commit. Before commit, restore the changed vault files from the temporary backup ZIP recorded in `AIEOS_OBSIDIAN_ID_NORMALIZATION_RUNTIME_REPORT.json` or use `git restore --pathspec-from-file=<runtime-index>`.
