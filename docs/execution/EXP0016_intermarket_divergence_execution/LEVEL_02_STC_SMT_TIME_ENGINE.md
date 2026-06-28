# Level 02 — STC Time Engine and Cycle Classifier

Status: implemented in patch `EXP0016_STC_SMT_LEVEL02_TIME_ENGINE`.

This level is still a no-trade layer. It does not build W highs/lows, does not detect SMT divergence, does not create signals, and does not send orders. Its only responsibility is to convert the terminal time into the canonical STC time model and to produce an auditable time/cycle stream.

## Why this level exists

The STC strategy is entirely time-driven. Every later decision depends on the correct New York trading-day classification:

- Whether the current moment belongs to the STC trading day.
- Whether the current moment is inside M1, M2, M3, or a no-entry gap.
- Which W cycle is active.
- Whether the current check candle is the final check candle of an M, which is not allowed to trigger entry.
- Whether the 15:30 New York hard-close zone is active.

If this layer is wrong, all later SMT and execution logic will be wrong even if the divergence code itself is correct.

## Canonical time model

The runtime starts from broker server time. The user supplies only the broker UTC offset:

`server_time = UTC + BrokerUtcOffsetHours`

The engine converts:

1. Server time to UTC.
2. UTC to New York wall-clock time.
3. New York wall-clock time to STC trading-day elapsed minutes from 20:00.

New York DST is handled inside the module using US DST rules:

- DST starts on the second Sunday of March at 02:00 New York local time.
- DST ends on the first Sunday of November at 02:00 New York local time.
- The UTC transition points are modeled as 07:00 UTC for the March switch and 06:00 UTC for the November switch.

## STC trading day

The STC trading day starts at 20:00 New York and ends at 15:30 New York the next calendar day.

The `stc_day_id` is the date of the 20:00 New York start, not the calendar date of the current timestamp.

Example:

- New York Monday 21:00 belongs to Monday's STC day.
- New York Tuesday 10:00 still belongs to Monday's STC day, because that day started Monday at 20:00.
- New York Tuesday 15:30 is the hard-close boundary for Monday's STC day.

## M cycle classification

The engine maps elapsed minutes from 20:00 into the following cycles:

- M1: 20:00 to 02:00, elapsed 0 to 360.
- Gap: 02:00 to 03:00, elapsed 360 to 420.
- M2: 03:00 to 09:00, elapsed 420 to 780.
- Gap: 09:00 to 09:30, elapsed 780 to 810.
- M3: 09:30 to 15:30, elapsed 810 to 1170.
- Hard-close zone / closed zone: 15:30 to 20:00.

No detection and no entry are allowed inside M gaps. Open positions are still managed in later levels.

## W cycle classification

Each active M has four 90-minute W cycles.

M1:

- W1: 20:00 to 21:30.
- W2: 21:30 to 23:00.
- W3: 23:00 to 00:30.
- W4: 00:30 to 02:00.

M2:

- W1: 03:00 to 04:30.
- W2: 04:30 to 06:00.
- W3: 06:00 to 07:30.
- W4: 07:30 to 09:00.

M3:

- W1: 09:30 to 11:00.
- W2: 11:00 to 12:30.
- W3: 12:30 to 14:00.
- W4: 14:00 to 15:30.

W1 will not produce signals in later levels, but Level 02 still classifies it because W1 levels become references for later W cycles.

## Check-candle anchoring

All check candles are anchored from the STC trading-day start at 20:00 New York.

For example, if the check candle is 10 minutes, the sequence is:

- 20:00 to 20:10
- 20:10 to 20:20
- 20:20 to 20:30
- and so on through the STC day.

This is independent from the chart timeframe.

## Final check candle rule

The final check candle of each M is not allowed to trigger entry.

The engine exposes:

- `final_check_of_m`
- `check_entry_allowed_at_close`

A check candle is entry-valid only if:

- Its start is inside an active M.
- Its close is strictly before the end of that M.
- It is not the final check candle of that M.

Therefore a check candle ending exactly at 02:00, 09:00, or 15:30 is not eligible for entry.

## Audit output

Level 02 writes:

- `stc_level02_build_sanity.csv`
- `stc_level02_runtime_events.csv`
- `stc_level02_time_audit.csv`

The time audit records:

- server time
- UTC time
- New York time
- New York DST flag
- STC day id
- elapsed minutes from 20:00
- phase
- M cycle
- W cycle
- M/W start and end times
- check candle start and end
- final-check flag
- entry-allowed-at-close flag
- hard-close due flag

## Acceptance criteria

Level 02 is accepted when:

1. The EA compiles.
2. It initializes with valid Symbol1/Symbol2 inputs.
3. It writes all three Level 02 CSV files to Common Files.
4. The time audit correctly classifies M1, M2, M3, the two M gaps, and the hard-close zone.
5. The New York DST flag changes correctly around DST transition dates.
6. Check candles are anchored from 20:00 New York.
7. Final check candles of M1, M2, and M3 are flagged as no-entry.
8. No signal, order, W high/low construction, or SMT detection exists yet.

## Next level

Level 03 should implement check-candle aggregation and data completeness logic for Symbol1 and Symbol2. It should still avoid SMT detection until W-level construction is ready.
