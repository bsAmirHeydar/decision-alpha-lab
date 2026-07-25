# Roll back UC-01

UC-01 adds its implementation, documentation and generated baseline records and modifies exactly eleven pre-existing Python files through bounded newline-literal syntax restoration. It performs no move or deletion.

## Before commit

Restore the eleven modified paths from `pre-unified-consolidation`, then remove the added paths listed in `UC01_COMMIT_FILE_INDEX.txt`. External preservation artifacts remain outside the repository and should be retained.

## After commit

Use a normal Git revert of the UC-01 commit. The pre-consolidation tag, archive branch, Git bundle and pre-patch source archive remain the authoritative recovery points for the original bytes.

Never delete the external Git bundle or source archives until the entire consolidation program is sealed and its retention policy has been approved.
