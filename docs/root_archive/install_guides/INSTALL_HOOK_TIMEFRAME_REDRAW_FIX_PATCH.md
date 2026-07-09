# Install Hook Timeframe Redraw Fix Patch

From the project root in Windows PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_timeframe_redraw_fix_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_timeframe_redraw_fix_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended debug inputs while testing:

```text
InpRuntimePrintRedrawState = true
InpPrintTimebaseSanity = true
InpPrintFailureSummaries = true
```

After testing, `InpRuntimePrintRedrawState` can be turned off again.
