# Install

Run from the project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_validity_no_draw_fix_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_validity_no_draw_fix_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```
