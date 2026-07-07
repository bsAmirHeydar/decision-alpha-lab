# Install — Strict Valid Hook View Fix

From the project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_strict_valid_hook_view_fix_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_strict_valid_hook_view_fix_patch.zip
```

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended inputs:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```

If you still see old objects after applying the patch, remove and reattach the expert once or change timeframe once. The patch also cleans Hook object prefixes on the next valid-only run.
