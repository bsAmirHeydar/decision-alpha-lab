# Hook Root Compile API Compatibility

## Error

`undeclared identifier 'FP_HookP02BuildSequencesWithRates'`

## Cause

Phase 03-06 still called the rate-aware Phase 02 entrypoint after the Phase 02 root rebuild replaced the internal sequence builder.

## Fix

Restore `FP_HookP02BuildSequencesWithRates(...)` as a compatibility wrapper in `FP_HookPhase02Rules.mqh`.

## Scope

Compile compatibility only.
