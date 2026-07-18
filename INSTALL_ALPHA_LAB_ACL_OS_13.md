# Install ACL-13 Patch

1. Place the ZIP in the repository root.
2. Expand it into the root with overwrite enabled.
3. Remove the ZIP.
4. Stage exact paths through `ACL_OS_13_FILE_INDEX.txt` using Git pathspec-from-file.
5. Commit using `COMMIT_MESSAGE.md` and push.

Rollback is a Git revert of the ACL-13 commit. The patch has no deletion manifest and does not modify unrelated experiment logic.
