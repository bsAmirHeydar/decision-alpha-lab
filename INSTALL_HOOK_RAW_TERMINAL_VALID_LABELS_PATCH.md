# Install — Hook Raw Terminal and Valid Labels Patch

From project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_raw_terminal_valid_labels_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_raw_terminal_valid_labels_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended final inputs:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```

For debugging:

```text
InpHookPhase02ExportCsv = true
InpHookPhase02PrintSummary = true
```
