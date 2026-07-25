# Install Alpha Lab LCM-12B

Apply the ZIP from the repository root using the provided PowerShell block. The block verifies the ZIP SHA-256, safely expands the payload, removes the ZIP, validates schemas and package digests, runs the LCM-12B acceptance suite and stable upstream regressions, stages exactly the paths listed in `LCM_12B_FILE_INDEX.txt`, checks the staged diff, commits with `COMMIT_MESSAGE_LCM_12B.md`, and pushes.

The canonical reconciliation root is:

`registry/legacy_context_migration/documentation_reconciliations/DOCRECON_F60803B1B8316F47D966D02CB905ACC8`
