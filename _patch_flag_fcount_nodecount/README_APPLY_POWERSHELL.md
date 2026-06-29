# Flag F-count vs Node-count Docs Correction Patch

Apply from the root of `decision-alpha-lab` in PowerShell.

```powershell
Expand-Archive -Path .\flag_fcount_vs_nodecount_docs_correction_patch.zip -DestinationPath .\_patch_flag_fcount_nodecount -Force
Remove-Item .\flag_fcount_vs_nodecount_docs_correction_patch.zip -Force
git apply .\_patch_flag_fcount_nodecount\flag_fcount_vs_nodecount_docs_correction.patch
```

Then review:

```powershell
git status
git diff --stat
```
