# Install — Hook Canon Step 1 Visible Set Patch

From the project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_canon_step1_visible_set_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_canon_step1_visible_set_patch.zip
```

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended production-valid-only inputs:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```
