# Install Hook Valid Cycles Only View Patch

Run from the project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_valid_cycles_only_view_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_valid_cycles_only_view_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended production inputs:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02ValidF3RequireOppositeDirection = false
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```

Debug fallback, only when diagnosing zero valid output:

```text
InpHookPhase02ValidOnlyFallbackToStructural = true
```
