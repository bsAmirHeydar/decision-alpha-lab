# INSTALL — Hook Canon Step 5 Closure and Strict Visible Set Patch

Run from the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_canon_step5_closure_strict_visible_set_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_canon_step5_closure_strict_visible_set_patch.zip
```

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended production-valid test inputs:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02ValidF3RequireOppositeDirection = true
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
InpHookPhase02RequireConfirmedResolveNode = true
InpHookPhase02ShowHookSequenceIdsInLabels = true
```
