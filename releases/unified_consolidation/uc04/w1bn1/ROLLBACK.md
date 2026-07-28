# Rollback

This patch adds files only. Before commit, delete every root-relative path in `PATCH_FILE_INDEX.txt`, processing files first and empty directories last.

After commit, use `git revert <commit>`; do not rewrite shared history. Native run evidence is outside the repository under `%LOCALAPPDATA%\AlphaLab\runs\uc04w1b` and may be removed independently.
