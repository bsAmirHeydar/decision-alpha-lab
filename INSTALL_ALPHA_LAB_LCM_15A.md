# Install Alpha Lab LCM-15A

Apply the ZIP from the repository root using the supplied PowerShell block. The workflow validates the exact ZIP digest and entry set, expands the patch, removes the ZIP, verifies the SHA-256 ledger, schemas, static authority boundary, package and installation, runs the direct LCM-15A suite and stable regressions, stages only the exact root-relative file index, verifies staged-path equality, commits and pushes.

LCM-15A creates evidence only. It does not relocate or delete candidate paths. `approved_relocation_pathspec.txt` is input for LCM-15B only; `approved_future_deletion_pathspec.txt` is intentionally empty.
