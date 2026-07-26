# Phase 06 Hotfix005 — Validation Plan

## 1. Clean Chart Test

1. Remove the EA from both charts.
2. Delete all objects whose name starts with `EXP0017_P06_`.
3. Attach the EA again.
4. Confirm that drawings appear before the attachment time.

## 2. Object List Test

Open Object List and verify that historical objects exist with suffixes such as:

```text
origin_to_destination_*
origin_marker_*
destination_marker_*
origin_vertical_*
destination_vertical_*
confirmation_close_vertical_*
reference_guide_*
current_extreme_guide_*
reference_cycle_anchor_*
visual_label_*
```

## 3. Backfill Summary Test

The Experts tab should print a summary similar to:

```text
EXP0017 Phase06 historical visual backfill complete: observations=600 drawn=... ledger=0 lookback_days=2 max_closed_candles=600 keep_first=true
```

## 4. First Confirmation Lock Test

With `InpKeepFirstVisualForSameSignalId = true`, lines should not migrate forward each timer pulse. If they keep moving, the primary object existence check is failing.

## 5. Performance Test

Start with:

```text
InpHistoricalBackfillLookbackTradingDays = 1
InpHistoricalBackfillMaxClosedCandles = 300
```

Then increase after confirming stability.

## 6. Dual Chart Test

Confirm that both input-symbol charts receive historical drawings, and that each chart receives only its own symbol-local price geometry.
