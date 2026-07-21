# EXP0017 Phase 10 Hotfix001 — MQL5 String Case Mutation

## Purpose
Fix MQL5 compile errors caused by using `StringToLower()` and `StringToUpper()` as value-returning functions.

## Root cause
In MQL5 these functions mutate a writable string variable and return a boolean success flag. They cannot receive a temporary expression as an lvalue and their return value cannot be assigned to a string.

## Correct pattern
```mql5
string value = CGM_Clean(source);
StringToUpper(value);
```

## Files changed
- `mql5/Include/IntermarketDivergenceExecution/CG/CGM_Types.mqh`
- `mql5/Include/IntermarketDivergenceExecution/CG/CGM_FeatureBuilder.mqh`

## Behavioral scope
No feature, label, ranking, dataset, model, strategy, order, risk, or execution behavior is changed. Only string normalization syntax is corrected.
