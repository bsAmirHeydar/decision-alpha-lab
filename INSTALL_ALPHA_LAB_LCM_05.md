# Install Alpha Lab LCM-05

Run from the repository root in PowerShell.

1. Verify the downloaded ZIP SHA-256.
2. Expand the patch into the repository root.
3. Remove the ZIP.
4. Verify the reference package and installation.
5. Run compileall and all direct/regression tests.
6. Stage exactly the paths listed by `LCM_05_FILE_INDEX.txt`.
7. Commit with `COMMIT_MESSAGE_LCM_05.md` and push.

The installation process does not move or delete existing legacy artifacts.
