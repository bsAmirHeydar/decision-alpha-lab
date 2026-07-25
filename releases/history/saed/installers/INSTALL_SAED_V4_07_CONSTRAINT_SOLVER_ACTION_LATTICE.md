# Installation

1. Place the ZIP patch in the repository root.
2. Expand it into the repository root with overwrite enabled.
3. Remove the ZIP from the root.
4. Run full QA and delivery validation.
5. Stage only paths listed in `SAED_V4_07_FILE_INDEX.txt`.
6. Review the staged diff, commit with `COMMIT_MESSAGE.md`, and push.

Rollback: revert the commit. Before commit, remove files in the file index and restore modified files from version control.
