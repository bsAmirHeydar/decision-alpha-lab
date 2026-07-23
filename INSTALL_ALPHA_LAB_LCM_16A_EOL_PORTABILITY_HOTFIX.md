# Install — LCM-16A EOL Portability Hotfix

Apply the ZIP from the repository root using the exact PowerShell workflow supplied with the release. The workflow:

1. verifies the ZIP SHA-256;
2. confirms the interrupted worktree contains only original LCM-16A paths;
3. overlays the hotfix;
4. verifies the hotfix hash ledger;
5. reruns LCM-16A QA, direct tests, historical tests, full regression, and engineering policy;
6. stages only the exact union of original LCM-16A and hotfix paths;
7. commits and pushes.
