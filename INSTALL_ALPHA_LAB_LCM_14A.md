# Install Alpha Lab LCM-14A

Apply the ZIP from the repository root with the supplied PowerShell block. The workflow validates the exact ZIP digest and entry set, expands the payload, removes the ZIP, verifies the hash ledger, schemas, static authority boundary, deprecation package and installation, executes the direct LCM-14A suite and stable regressions, stages only the exact root-relative file index, verifies staged-path equality, commits and pushes.

The installation does not activate compatibility redirects in production and does not grant quarantine, deletion, runtime, order or capital authority.
