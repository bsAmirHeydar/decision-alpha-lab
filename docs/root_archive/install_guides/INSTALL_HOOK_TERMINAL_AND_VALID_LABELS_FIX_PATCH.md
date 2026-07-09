# Install Hook Terminal and Valid Labels Fix Patch

From the repository root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_terminal_valid_labels_fix_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_terminal_valid_labels_fix_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```
