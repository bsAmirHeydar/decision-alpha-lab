# Phase 10 Hotfix001 — MQL5 String Case Mutation

## Failure signature

The Phase 10 model-dataset expert failed with `lvalue expected` and implicit `unknown` to `string` conversion diagnostics around `StringToLower()` and `StringToUpper()`.

## Root cause

MQL5 string case functions are in-place mutators:

```mql5
bool StringToLower(string& value);
bool StringToUpper(string& value);
```

The original implementation treated them as if they returned transformed strings:

```mql5
string normalized = StringToUpper(CGM_Clean(source));
```

This violates two contracts:

1. `CGM_Clean(source)` is a temporary expression, not a writable lvalue.
2. The return type is `bool`, not `string`.

## Corrected contract

Normalization now occurs in two explicit steps:

```mql5
string normalized = CGM_Clean(source);
StringToUpper(normalized);
```

## Corrected locations

- Boolean parsing in `CGM_ToBool()`.
- Direction normalization in `CGM_DirectionCode()`.
- Side normalization in `CGM_SideCode()`.
- Outcome availability normalization in `CCGM_FeatureBuilder::BuildRow()`.

## Invariants preserved

- `true`, `1`, and `yes` remain truthy after trimming and lowercase normalization.
- `BUY` maps to `1`; `SELL` maps to `-1`.
- `LOW` maps to `1`; `HIGH` maps to `-1`.
- Complete outcomes remain identified by case-insensitive comparison with `COMPLETE`.
- No dataset schema or label semantics change.
