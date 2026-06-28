# 03 - Cycle Calendar and Time Model

## 1. Time authority

All strategy times are defined in New York time.

The implementation must support New York DST. Broker time must be converted into New York time through a broker-to-UTC offset and a New-York DST conversion layer.

For external CME or CSV data, the preferred storage time is UTC. The strategy layer converts UTC to New York time for cycle assignment.

## 2. STC trading day

The STC trading day starts at 20:00 New York and ends at 15:30 New York the following calendar day.

The trading-day label is the date of the 15:30 hard close. For example, the STC day that starts Monday 20:00 and ends Tuesday 15:30 is Tuesday's STC trading day.

No strategy decision may use candles before the start of the current STC trading day.

## 3. Daily reset

At 15:30 New York:

1. All open STC positions must be hard-closed.
2. All active divergences are cleared.
3. All cycle states are reset.
4. All trade counters are reset.
5. All partial state flags are reset for the next day.
6. No position may remain open after the close process is complete.

If hard close is missed because the EA is offline, the first restart after 15:30 must enter hard-close recovery mode.

## 4. M cycles

M1 runs from 20:00 to 02:00.

M2 runs from 03:00 to 09:00.

M3 runs from 09:30 to 15:30.

M cycles do not overlap. Direction lock, trade count, W references, and divergence scope are local to each M.

## 5. No-entry gaps

Gap 1: 02:00 to 03:00.

Gap 2: 09:00 to 09:30.

During gaps, the signal engine does not detect new SMT divergence and the entry engine does not enter. The position-management engine remains active.

The system may still need data in gaps for position outcomes. If TP or SL is hit during a gap, the trade outcome is recorded. If a delayed hard close or delayed partial is required, management actions are allowed.

## 6. W cycles

Every M contains four W cycles, each 90 minutes long.

M1:

| W | Start | End |
|---|---:|---:|
| W1 | 20:00 | 21:30 |
| W2 | 21:30 | 23:00 |
| W3 | 23:00 | 00:30 |
| W4 | 00:30 | 02:00 |

M2:

| W | Start | End |
|---|---:|---:|
| W1 | 03:00 | 04:30 |
| W2 | 04:30 | 06:00 |
| W3 | 06:00 | 07:30 |
| W4 | 07:30 | 09:00 |

M3:

| W | Start | End |
|---|---:|---:|
| W1 | 09:30 | 11:00 |
| W2 | 11:00 | 12:30 |
| W3 | 12:30 | 14:00 |
| W4 | 14:00 | 15:30 |

## 7. W high and low construction

A W is treated as a synthetic 90-minute candle.

The high of a W is the maximum high inside the W interval.

The low of a W is the minimum low inside the W interval.

The final W high and W low should not depend on the timeframe used, as long as the data fully covers the W interval. Therefore the implementation may build W levels from M1, aggregated check candles, or available lower timeframe data.

If data for either symbol is incomplete, the W is marked incomplete and no SMT signal can depend on it.

## 8. Check candle anchoring

All check candles are anchored from the STC trading-day start, 20:00 New York.

For example, with a 10-minute check candle:

- 20:00-20:10.
- 20:10-20:20.
- 20:20-20:30.

The same anchoring applies to 1m, 3m, 5m, 15m, and 30m.

This rule avoids broker-chart timeframe dependency.

## 9. Last check candle rule

The last check candle of each M is not allowed to produce an entry.

If confirmation close time is equal to or later than the M end time, the signal expires.

Examples:

- In M1, a check candle that closes at 02:00 cannot enter.
- In M2, a check candle that closes at 09:00 cannot enter.
- In M3, a check candle that closes at 15:30 cannot enter because hard close dominates.

## 10. Cycle assignment algorithm

For each bar timestamp:

1. Convert timestamp to New York time.
2. Determine current STC trading day.
3. If time is before 20:00 and after 15:30 for the active STC day, it belongs to no active signal window.
4. Assign the bar to M1, M2, M3, or gap.
5. If inside an M, assign the bar to W1, W2, W3, or W4.
6. Assign the bar to the active check candle bucket anchored from 20:00.
7. Mark whether the current check candle is final for its M.

## 11. Data completeness algorithm

For each symbol and each W/check-candle interval:

1. Count expected bars for the data granularity.
2. Count actual bars.
3. If either symbol is missing required data, mark the interval incomplete.
4. If the interval is incomplete, no signal may be generated from it.
5. Incomplete intervals are still written to audit output with reason `DATA_INCOMPLETE`.
