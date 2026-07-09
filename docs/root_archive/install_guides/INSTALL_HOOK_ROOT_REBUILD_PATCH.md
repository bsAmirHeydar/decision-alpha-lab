# Install Hook Root Rebuild Patch

PowerShell from project root:

```powershell
Expand-Archive -Path .\alpha_lab_hook_root_rebuild_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_root_rebuild_patch.zip
```

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```
