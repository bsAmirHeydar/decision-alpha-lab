# Install Hook Validity Lite Compile Fix Patch

From project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_validity_lite_compile_fix_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_validity_lite_compile_fix_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```
