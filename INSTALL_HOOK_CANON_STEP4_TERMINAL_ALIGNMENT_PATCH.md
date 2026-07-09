# Install Hook Canon Step 4 Patch

From the project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_canon_step4_terminal_alignment_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_canon_step4_terminal_alignment_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended inputs for canonical valid-only testing:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02ValidF3RequireOppositeDirection = true
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
InpHookPhase02ShowHookSequenceIdsInLabels = true
```
