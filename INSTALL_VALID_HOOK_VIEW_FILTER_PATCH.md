# Install — Valid Hook View Filter Patch

From the project root in Windows PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_valid_hook_view_filter_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_valid_hook_view_filter_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended production input:

```text
InpHookPhase02ShowOnlyValidHooks = true
```

Recommended debug input:

```text
InpHookPhase02ShowOnlyValidHooks = false
InpHookPhase02PrintSummary = true
InpHookPhase02ExportCsv = true
```
