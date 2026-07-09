# Install

From the repository root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_canon_step7_post_f3_recognition_code_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_canon_step7_post_f3_recognition_code_patch.zip
```

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended test inputs:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPostF3RecognitionMode = FP_HOOK_POST_F3_STRUCTURAL_OR_GEOMETRIC_80
InpHookPostF3SelectionPriority = FP_HOOK_POST_F3_PRIORITY_STRUCTURAL_FIRST
InpHookPostF3AllowDirectTerminalHook = true
InpHookPostF3AllowDelayedReboundHook = true
InpHookPostF3MaxSearchBars = 180
InpHookPostF3TerminalToleranceBars = 3
InpHookPostF3TerminalTolerancePricePoints = 20
InpHookPostF3GeometricMinCompletionPct = 80.0
```
