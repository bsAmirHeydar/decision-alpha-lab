# Installation

Run from the repository root after placing the root-relative ZIP there.

1. Extract the ZIP into the repository root.
2. Remove the ZIP.
3. Run `releases/unified_consolidation/ci_recovery_04/APPLY.ps1`.
4. Stage only paths listed in `PATCH_FILE_INDEX.txt`.
5. Commit only after every gate reports PASS.

The verifier does not require Git LFS checkout representation to be pointer-only. Existing hydrated-object validation remains unchanged.
