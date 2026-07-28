# Installation

Place the ZIP in the repository root. From that root, expand it, delete the ZIP, and execute `releases/unified_consolidation/uc04/w1bn1/APPLY.ps1`. The installer verifies the exact patch hashes and runs all mandatory upstream and stage gates.

After all gates pass, stage only `PATCH_FILE_INDEX.txt` and commit with `COMMIT_MESSAGE.txt`. Push is deliberately excluded.

The later native Windows run is separate:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "tools/consolidation/uc04w1bn1/Invoke-UC04W1BNativeHostQualification.ps1" -RepositoryRoot (Get-Location).Path -RuntimeSymbol "#USSPX500"
```
