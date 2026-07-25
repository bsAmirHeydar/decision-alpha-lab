# LCM-10A Installation and Validation

Apply the release ZIP from the repository root with PowerShell. The installation sequence must:

1. expand the patch atomically into the repository root;
2. remove the consumed ZIP;
3. compile the LCM-10A Python package;
4. verify the patch hash ledger;
5. validate every published schema;
6. run the static authority boundary validator;
7. verify the generated inventory package and its manifest chain;
8. verify the repository installation against the exact path index;
9. run LCM-10A QA;
10. run direct LCM-10A tests and upstream regression tests;
11. stage only paths from `LCM_10A_FILE_INDEX.txt`;
12. run Git whitespace validation;
13. commit with `COMMIT_MESSAGE_LCM_10A.md` and push.

Do not use `git add .` or `git add -A`. Do not delete or relocate legacy source files. A failed verification must stop the workflow before staging or committing.
