# Apply Flag Reverse Extreme Fractal Entry Philosophy Patch

Run these commands from the root of `decision-alpha-lab` in Windows PowerShell.

```powershell
Expand-Archive -Path .\flag_reverse_extreme_fractal_entry_philosophy_patch.zip -DestinationPath .\_patch_flag_reverse_extreme -Force
Remove-Item .\flag_reverse_extreme_fractal_entry_philosophy_patch.zip -Force
git apply .\_patch_flag_reverse_extreme\flag_reverse_extreme_fractal_entry_philosophy.patch
```

Check:

```powershell
git status
git diff --stat
```
