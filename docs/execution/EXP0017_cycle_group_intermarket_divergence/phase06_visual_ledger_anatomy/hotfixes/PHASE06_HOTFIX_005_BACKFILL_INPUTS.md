# Phase 06 Hotfix005 — Backfill Input Catalog

## `InpEnableHistoricalVisualBackfill`

Enables the historical scan. Recommended default: `true`. Disable it only when debugging live-only performance or when the chart already contains enough objects.

## `InpHistoricalBackfillLookbackTradingDays`

Defines how far back the scan should look. Recommended starting value: `2`. For M1 charts, larger values can create many objects and should be tested carefully.

## `InpHistoricalBackfillMaxClosedCandles`

Hard limit on closed-candle observations. Recommended starting value: `600`. This prevents the EA from scanning too much history on attach.

## `InpHistoricalBackfillWriteLedger`

Default: `false`. Historical drawing is useful immediately; historical ledger writing can create many rows. Keep false until the visual layer is validated.

## `InpHistoricalBackfillPrintSummary`

Default: `true`. Prints observation count, drawn count, ledger count, lookback days, maximum candles, and first-visual lock state.

## `InpKeepFirstVisualForSameSignalId`

Default: `true`. Keeps the first historical confirmation position. This is essential for visual correctness because the same signal id may be reconstructed on multiple subsequent closed candles inside the same CG cycle.
