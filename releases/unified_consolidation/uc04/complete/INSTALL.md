# Install

Extract the ZIP into a temporary staging directory, then run `APPLY.ps1 -Action Install -RepositoryRoot <repo> -StagingRoot <staging>`. The installer validates exact membership and hashes, backs up every target, copies atomically, executes all static gates and rolls back automatically on failure.

After the patch is committed, run `tools/consolidation/uc04complete/Invoke-UC04CompleteNativeSeal.ps1 -RepositoryRoot <repo> -RuntimeSymbol "#USSPX500" -FinalizeRepository`. Commit the two generated acceptance records only after the native runner reports PASS.
