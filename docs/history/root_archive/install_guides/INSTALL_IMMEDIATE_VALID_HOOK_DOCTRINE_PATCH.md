# Install

From the project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_immediate_valid_hook_doctrine_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_immediate_valid_hook_doctrine_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```
