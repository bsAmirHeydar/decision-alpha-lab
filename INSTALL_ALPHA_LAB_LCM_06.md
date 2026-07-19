# Install Alpha Lab LCM-06

Run the final PowerShell block from the repository root.

The installation procedure:

1. verifies the downloaded ZIP SHA-256 before extraction;
2. expands the root-relative patch and removes the ZIP;
3. verifies the immutable LCM-06 reference framework;
4. verifies every path listed in `LCM_06_FILE_INDEX.txt`;
5. runs the phase QA command;
6. compiles the LCM-06 Python package;
7. runs direct LCM-06 tests and all bounded regression suites from LCM-05 through LCM-00 plus ACL-15;
8. stages only the exact file index using Git pathspec-from-file;
9. commits with `COMMIT_MESSAGE_LCM_06.md` and pushes.

The patch does not move, delete, merge, refactor or cut over any legacy artifact. No MetaTrader compiler or runtime claim is made by this installation procedure.
