# 03 - STC Cycle Calendar

## 1. Canonical time zone

All cycle times are New York times.

```text
America/New_York
```

The EA must handle DST automatically.

## 2. STC day

```text
20:00 New York -> 15:30 New York next day
```

The source SRS is explicit that the strategy uses only the current trading day and resets at 15:30.

## 3. M cycles

| M | Start NY | End NY | Duration | Notes |
| --- | --- | --- | --- | --- |
| M1 | 20:00 | 02:00 | 6h | crosses midnight |
| M2 | 03:00 | 09:00 | 6h | after 1h gap |
| M3 | 09:30 | 15:30 | 6h | ends at STC day reset |

## 4. Gaps

The PDF does not define behavior for:

| Gap | NY time |
| --- | --- |
| Gap 1 | 02:00 -> 03:00 |
| Gap 2 | 09:00 -> 09:30 |

Recommended implementation until clarified:

- No new divergence detection inside gaps.
- Open trades continue to be managed.
- If a check candle closes inside a gap, it should be handled only if its pending divergence was created in the previous active W and the confirmation candle was already scheduled before the gap.

This must be confirmed before production code.

## 5. W cycles

### M1

| W | Start NY | End NY |
| --- | --- | --- |
| W1 | 20:00 | 21:30 |
| W2 | 21:30 | 23:00 |
| W3 | 23:00 | 00:30 |
| W4 | 00:30 | 02:00 |

### M2

| W | Start NY | End NY |
| --- | --- | --- |
| W1 | 03:00 | 04:30 |
| W2 | 04:30 | 06:00 |
| W3 | 06:00 | 07:30 |
| W4 | 07:30 | 09:00 |

### M3

| W | Start NY | End NY |
| --- | --- | --- |
| W1 | 09:30 | 11:00 |
| W2 | 11:00 | 12:30 |
| W3 | 12:30 | 14:00 |
| W4 | 14:00 | 15:30 |

## 6. W level construction

For each symbol and every W:

```text
W High = maximum high inside W interval
W Low  = minimum low inside W interval
```

Recommended interval policy:

```text
start inclusive, end exclusive
```

Example:

```text
M3.W1 includes bars with NY open time >= 09:30 and < 11:00.
M3.W2 includes bars with NY open time >= 11:00 and < 12:30.
```

## 7. Check-candle interaction

`Candle Check` defines how long the EA waits after raw divergence formation before validating entry.

Allowed check durations:

```text
1m, 3m, 5m, 10m, 15m, 30m
```

At the check candle close, the divergence is either confirmed or canceled.

## 8. End of W4 behavior

At the end of W4 for each M:

- perform partial-close checks for trades opened in that M;
- preserve M-local counters until the M fully ends;
- then close the M cycle state.

At the end of M3.W4, this also coincides with the end-of-day reset at 15:30.
