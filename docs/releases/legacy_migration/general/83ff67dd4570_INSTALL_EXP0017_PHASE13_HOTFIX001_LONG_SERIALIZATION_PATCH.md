# EXP0017 Phase 13 Hotfix001 — MQL5 Long Serialization

## Purpose

Fix the MetaEditor compile failure in `CGP13_Writers.mqh` caused by the unsupported identifier `LongToString`.

## Root cause

`SCGP13FileRow::size_bytes` is a `long`. In MQL5, `IntegerToString` accepts an integer/long value, while `LongToString` is not available in the target compiler. The parser failure at that expression caused the remaining operator errors and warnings on the surrounding concatenation.

## Change

```mql5
// Before
LongToString(rows[i].size_bytes)

// After
IntegerToString(rows[i].size_bytes)
```

## Scope

Only the CSV serialization of `size_bytes` is changed. No Phase 13 model logic, fold logic, Python logic, integrity gate, strategy behavior, signal behavior, risk behavior, or execution behavior is changed.

## Validation

Recompile:

`mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Controlled_Model_Comparison_Bridge.mq5`

Expected result:

`0 errors, 0 warnings`
