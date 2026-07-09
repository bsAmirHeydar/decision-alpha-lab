# Phase 06 Hotfix 001 Dependency Map

```text
CGV_Types.mqh
  -> CGC_Types.mqh

CGV_Ledger.mqh
  -> CGV_Types.mqh
  -> CGC_ConfirmationField.mqh

CGV_Drawing.mqh
  -> CGV_Types.mqh
  -> CGC_ConfirmationField.mqh

CGV_Engine.mqh
  -> CGT_Time.mqh
  -> CGV_Display.mqh
  -> CGV_Drawing.mqh
  -> CGC_ConfirmationField.mqh through visual modules
```

Compile failure pattern:

```text
missing CGC include
  -> unknown SCGCFinalSignal
  -> unknown enum constants
  -> declaration without type
  -> reference syntax errors
  -> undeclared identifier cascade
```

Correction:

```text
restore Phase 05 CGC include files
```
