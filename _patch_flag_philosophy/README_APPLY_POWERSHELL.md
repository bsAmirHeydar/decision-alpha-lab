# Flag Market Anatomy Philosophy Patch

Apply from the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path .\flag_market_anatomy_philosophy_patch.zip -DestinationPath .\_patch_flag_philosophy -Force
Remove-Item .\flag_market_anatomy_philosophy_patch.zip -Force
git apply .\_patch_flag_philosophy\flag_market_anatomy_philosophy.patch
```

Then review and commit:

```powershell
git status
git diff --stat
```
