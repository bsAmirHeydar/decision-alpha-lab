# Level 04 — W Level Builder

## Status

Level 04 adds the first structural market object required by STC: the closed 90-minute W high/low levels for both symbols.

This level is still non-trading. It does not detect SMT, confirm signals, simulate entries, draw objects, open positions, partial-close positions, or hard-close positions. It only builds and audits W levels after each W closes.

## Why this level exists

STC does not compare raw prices between SPX and NDX. It compares each symbol against its own W reference levels. Therefore the system needs a deterministic W-level layer before SMT can exist.

The locked owner rule is:

- each symbol has its own W high and W low;
- the comparison is structural, not price-shared;
- W1 gives no signal;
- W2 may later compare only with W1;
- W3 may later compare with W2 and W1;
- W4 may later compare with W3, W2 and W1;
- no W compares with itself;
- W high/low is the high/low of the whole 90-minute synthetic candle;
- the construction timeframe does not change the meaning of the level, but the implementation uses M1 bars for deterministic audit.

## Output file

The new audit file is written under the Common Files root:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level04_w_levels.csv`

It contains one row per closed W:

- STC day id;
- W serial from 0 to 11;
- M cycle;
- W cycle;
- W start/end in New York time;
- W start/end in broker server time;
- whether the W is closed;
- whether W1 has no signal;
- whether this W can serve as a future reference inside the same M;
- the reference set that would be allowed while trading inside that W;
- OHLCV for Symbol1 over the 90-minute W;
- OHLCV for Symbol2 over the 90-minute W;
- data completeness for both symbols.

## W serial map

| Serial | M | W | New York interval |
|---:|---|---|---|
| 0 | M1 | W1 | 20:00-21:30 |
| 1 | M1 | W2 | 21:30-23:00 |
| 2 | M1 | W3 | 23:00-00:30 |
| 3 | M1 | W4 | 00:30-02:00 |
| 4 | M2 | W1 | 03:00-04:30 |
| 5 | M2 | W2 | 04:30-06:00 |
| 6 | M2 | W3 | 06:00-07:30 |
| 7 | M2 | W4 | 07:30-09:00 |
| 8 | M3 | W1 | 09:30-11:00 |
| 9 | M3 | W2 | 11:00-12:30 |
| 10 | M3 | W3 | 12:30-14:00 |
| 11 | M3 | W4 | 14:00-15:30 |

## Completeness rule

A W level is complete only when both symbols have the expected 90 M1 bars covering the W interval.

If either symbol is incomplete, the W row is still audited, but the W is marked as not usable as a future reference.

## Reference role

A closed W is only a level object at this stage. It does not create a signal by itself.

W1 is built but cannot produce a signal while it is the current W. It is still important because it becomes the first reference for W2, W3 and W4.

W4 is built for audit and later position-management context, but it has no later W inside the same M. Therefore it is not a future reference inside that M.

## Level 04 acceptance criteria

The level is accepted when:

1. The EA compiles.
2. The EA initializes with Level 04 sanity output.
3. `stc_level04_w_levels.csv` is created.
4. Closed W rows appear after W close times.
5. W rows are anchored to New York STC time, not chart time.
6. Each W row contains separate OHLCV for Symbol1 and Symbol2.
7. W1 is marked as no-signal.
8. Missing data on either symbol marks the pair as incomplete.
9. No SMT candidate, signal, paper trade, or order is produced.
