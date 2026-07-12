# F2 Waist Limit — Validation Plan

## Compile

Compile both files:

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5
```

The second compile verifies that reuse of Phase 52 generic helpers did not regress the existing Hook profile.

## Positive cases

1. Bullish confirmed F2 with F1 waist below the F2-waist entry and F2 Leg2 above entry.
2. Bearish mirrored geometry.
3. Fixed-volume order accepted with SL and TP attached.
4. Risk-cash sizing accepted.
5. Pending order blocks a second F2.
6. Filled position blocks a second F2.
7. Detector fast path activates while exposure exists.

## Negative cases

1. F2 candidate not confirmed.
2. F2 has no canonical parent F1.
3. Parent F1 waist unavailable.
4. F1 waist is on the wrong side of entry.
5. F2 Leg2 is on the wrong side of entry.
6. Exact SL or TP violates broker stops level.
7. Limit is no longer on the legal side of Bid/Ask.
8. Old F2 exceeds setup-age window.
9. Same F2 already consumed.
10. Foreign symbol position exists.

## Parity checks

For each accepted setup, compare against the production detector event stream:

```text
F2 event id
sequence id
direction
F2 confirmation time
F2 waist
parent F1 waist
F2 Leg2
```
