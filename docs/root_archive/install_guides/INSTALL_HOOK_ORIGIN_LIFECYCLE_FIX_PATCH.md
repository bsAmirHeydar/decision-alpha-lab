# Install Hook Origin Lifecycle Fix Patch

Place the zip in the project root and run in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_origin_lifecycle_fix_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_origin_lifecycle_fix_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Keep this input enabled for production interpretation:

```text
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```
