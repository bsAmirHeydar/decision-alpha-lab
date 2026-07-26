# Level 03 — Check Candle Aggregator and Pair Data Completeness

## Purpose

Level 03 adds the first data layer on top of the Level 02 time engine. The strategy still does not detect SMT, does not construct W reference levels, does not create signals, does not simulate trades, and does not send orders.

The only job of this level is to convert raw M1 broker data for `Symbol1` and `Symbol2` into deterministic STC check candles aligned from the 20:00 New York STC trading-day anchor.

This is the layer that makes later SMT detection safe. If the two-symbol check candle is not complete, no later signal layer is allowed to use it.

## Locked owner decisions implemented here

The following owner decisions are encoded in this level:

- Check candles are anchored from 20:00 New York.
- Supported check sizes are 1m, 3m, 5m, 10m, 15m, and 30m.
- Check candles are internally aggregated from M1 data.
- Both symbols must have complete data for a check candle to be eligible.
- Gap periods are no-entry and no-detection zones.
- No data is intentionally extracted from gap check candles for signal detection.
- Final check candles of each M are audited but cannot produce entries in later layers.
- Symbol1 and Symbol2 are both the data symbols and the execution symbols.
- Level 03 remains no-trade and no-signal.

## Check candle anchoring

Every check candle is anchored from the STC trading day start:

- STC trading day start: 20:00 New York.
- Check index 0 starts at 20:00.
- Check index 1 starts at `20:00 + check_minutes`.
- The sequence continues through the active STC day.

For a 10-minute check candle, the first candles are:

- 20:00–20:10
- 20:10–20:20
- 20:20–20:30

The anchor is never the chart open time and never the EA attach time.

## Aggregation algorithm

For each closed check candle:

1. Compute the check candle start and end in New York time.
2. Convert the start and end to broker server time through the Level 02 broker/UTC/New-York model.
3. Read M1 bars for Symbol1 over `[start, end)`.
4. Read M1 bars for Symbol2 over `[start, end)`.
5. Aggregate each symbol independently:
   - Open = first M1 open.
   - High = maximum M1 high.
   - Low = minimum M1 low.
   - Close = last M1 close.
   - Tick volume = sum of M1 tick volumes.
   - Real volume = sum of M1 real volumes.
   - Spread max = maximum observed M1 spread.
6. Mark each symbol complete only if the expected number of M1 bars exists and time coverage matches the interval.
7. Mark the pair complete only when both symbols are complete.
8. Write one row to the check candle audit journal.

## Completeness rule

For a check candle of size `N` minutes, the expected number of M1 bars is `N`.

A symbol check candle is complete only when:

- actual M1 bar count equals expected M1 bar count,
- the first M1 bar covers the check start,
- the last M1 bar reaches the expected last M1 open time.

A pair check candle is complete only when both Symbol1 and Symbol2 are complete.

Later signal layers must reject any check candle where pair completeness is false.

## Active-M and gap behavior

Level 03 classifies every closed check candle by its start time.

If the check start is inside M1, M2, or M3, the candle is eligible for aggregation.

If the check start is inside an M gap, the candle is not used for data extraction for signal detection. The audit marks the skip reason as a gap/no-data-extraction condition.

This matches the locked rule that gap periods do not create entries and do not need detection data.

## Final check behavior

A check candle whose close is at or beyond the end of its M is marked as final.

Final check candles are audited because they matter for boundary validation and future position-management logic, but they cannot create entries in later signal layers.

Examples:

- 01:55–02:00 is the final check of M1 for 5m mode.
- 08:55–09:00 is the final check of M2 for 5m mode.
- 15:25–15:30 is the final check of M3 for 5m mode.

## Runtime behavior

Level 03 runs on the EA timer.

On every pulse:

1. Refresh the duplicate-instance lock.
2. Refresh the Level 02 time snapshot.
3. Write time audit if enabled.
4. Determine the latest closed check candle.
5. Backfill/catch up any closed check candles not yet audited.
6. Write check candle audit rows.
7. Write heartbeat events.

No ticks are used for signal decisions in this level.

## Backfill and catch-up

Two inputs control catch-up behavior:

- `InpMaxCheckBackfillOnInit`
- `InpMaxCheckCatchupPerPulse`

When the EA starts in the middle of an STC day, it can backfill recent closed check candles for audit.

On each pulse, it processes up to the configured catch-up limit so the EA does not freeze when many candles are missing from the audit.

This is only an audit/data layer. It does not create delayed entries.

## Output file

The new output is written to Common Files:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_check_candles.csv`

Each row contains:

- STC day id,
- check index,
- check start/end in New York time,
- check start/end in broker server time,
- M and W classification,
- final-check flag,
- entry-allowed-at-close flag,
- data completeness flags,
- Symbol1 OHLCV aggregate,
- Symbol2 OHLCV aggregate,
- skip or eligibility reason.

## Acceptance criteria

Level 03 is accepted only when:

- The EA compiles.
- The EA still produces no signals and no orders.
- Check candles are aligned from 20:00 New York.
- Check candles use M1 data, not chart timeframe data.
- Both symbols are audited separately.
- Pair completeness is false when either symbol is incomplete.
- Gap check candles do not extract data for signal detection.
- Final check candles are marked as no-entry.
- The check candle CSV is deterministic and readable.
