# Phase 07 Validation and Test Plan

## Test 1 — No trading

Compile and attach `EXP0017_CG_Outcome_Study_Anatomy.mq5`. Confirm that no `CTrade`, order send, position close, or modification function exists.

## Test 2 — CSV creation

Confirm that `EXP0017_Phase07_Outcome_Study.csv` is created under terminal files or common files depending on input.

## Test 3 — Confirmed-only population

Outcome rows must only be written for `CGC_STATUS_CONFIRMED_TRADEABLE` signals. Invalidated double-hunt audit states are not outcome rows in this phase.

## Test 4 — Stop-distance sanity

For BUY signals, stop should be below or near entry as the clean reference low. For SELL signals, stop should be above or near entry as the clean reference high. Zero or malformed risk rows must be marked `ZERO_RISK` or `MISSING_DATA`.

## Test 5 — Window correctness

Compare one visible signal manually:

- confirmation close
- cycle-end price
- day-end price
- MFE high/low
- MAE high/low

## Test 6 — No strategy mutation

Changing outcome inputs must not change signal generation logic. It can only change measurement output.
