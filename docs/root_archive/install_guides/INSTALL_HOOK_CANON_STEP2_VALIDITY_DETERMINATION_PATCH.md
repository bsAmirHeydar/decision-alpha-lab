# Install — Hook Canon Step 2 Validity Determination Patch

From the project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_canon_step2_validity_determination_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_canon_step2_validity_determination_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

After compile, test with CSV enabled:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ExportCsv = true
InpHookPhase02PrintSummary = true
```

Inspect:

```text
hook_phase02_sequences.csv
hook_phase02_summary.csv
```

Expected valid families:

```text
HOOK_AFTER_OPPOSING_F3_TERMINAL
HOOK_AFTER_HOOK
HOOK_AFTER_HOOK_AND_OPPOSING_F3_TERMINAL
```
