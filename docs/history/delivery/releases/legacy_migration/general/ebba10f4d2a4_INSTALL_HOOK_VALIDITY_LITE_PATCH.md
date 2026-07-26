# Install Hook Validity Lite Patch

From the project root in PowerShell:

```powershell
Expand-Archive -Path .lpha_lab_hook_validity_lite_patch.zip -DestinationPath . -Force
Remove-Item .lpha_lab_hook_validity_lite_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended valid-only inputs:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```
