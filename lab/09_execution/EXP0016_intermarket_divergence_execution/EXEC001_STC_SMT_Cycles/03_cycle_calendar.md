# 03 - STC Cycle Calendar

## Timezone

All strategy times are expressed in New York time.

The implementation must handle New York DST correctly.

For broker-based MQL5 execution, the user provides broker UTC offset. For CME/CSV/Python tooling, UTC timestamps should be converted to New York for cycle assignment.

## STC trading day

The STC trading day starts at 20:00 New York and ends at 15:30 New York on the following calendar day.

No previous-day state is used after daily reset.

## M cycle layout

M1 runs from 20:00 to 02:00.

M2 runs from 03:00 to 09:00.

M3 runs from 09:30 to 15:30.

## Gap rules

02:00 -> 03:00 is a no-entry and no-detection gap.

09:00 -> 09:30 is a no-entry and no-detection gap.

During these gaps, position management remains active only for already-open trades, especially final TP processing.

No new STC entries are allowed in gaps.

## M1 W cycles

W1: 20:00 -> 21:30

W2: 21:30 -> 23:00

W3: 23:00 -> 00:30

W4: 00:30 -> 02:00

Partial check for M1 occurs at 02:00.

## M2 W cycles

W1: 03:00 -> 04:30

W2: 04:30 -> 06:00

W3: 06:00 -> 07:30

W4: 07:30 -> 09:00

Partial check for M2 occurs at 09:00.

## M3 W cycles

W1: 09:30 -> 11:00

W2: 11:00 -> 12:30

W3: 12:30 -> 14:00

W4: 14:00 -> 15:30

M3 end occurs at 15:30. Daily hard close overrides practical partial-close usefulness at that time.

## W candle definition

Each W is a synthetic 90-minute candle.

For each symbol and W:

- W open time is fixed by the calendar.
- W close time is fixed by the calendar.
- W high is the maximum high inside the W interval.
- W low is the minimum low inside the W interval.

The data timeframe used to derive W highs and lows is implementation-dependent, as long as the resulting W high/low is accurate.

## Eligibility by W

W1 has no eligible reference W and does not generate signals.

W2 eligible references:

- W1

W3 eligible references:

- W2
- W1

W4 eligible references:

- W3
- W2
- W1

Current W is never eligible as its own reference.

No reference can come from a different M.

No reference can come from a previous trading day.

## Last-check-candle rule

The last check candle that would close exactly at an M end is not allowed to create a new entry.

At M1 end, the time is for M1 partial processing.

At M2 end, the time is for M2 partial processing.

At M3 end, the time is for daily hard close and reset.
