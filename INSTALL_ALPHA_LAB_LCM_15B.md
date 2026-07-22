# Install Alpha Lab LCM-15B

Apply the ZIP from the repository root using the supplied PowerShell workflow. The workflow verifies the ZIP, expands it, removes the ZIP, validates hashes, schemas, static authority boundaries, package and installation, runs direct and stable regression suites, stages only `LCM_15B_FILE_INDEX.txt`, verifies exact staged-path equality, commits and pushes.
