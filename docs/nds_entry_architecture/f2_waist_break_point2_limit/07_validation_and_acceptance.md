# 07 — Validation and Acceptance

## Structural acceptance

1. F2 body is complete and unconfirmed.
2. Direct parent F1 is confirmed.
3. Point 1 equals `f2.waist`.
4. Entry is strictly beyond Point 1.
5. Stop is strictly beyond `f1.waist`.
6. Target equals `f2.leg2`.
7. F2 confirmation is not used as the entry trigger.

## Bullish golden case

```text
F1 waist = 100
F2 waist = 110
F2 Leg2 = 130
trade tick = 1
entry ticks = 1
stop ticks = 1

Buy Limit = 109
SL = 99
TP = 130
```

## Bearish golden case

```text
F1 waist = 130
F2 waist = 120
F2 Leg2 = 100
trade tick = 1
entry ticks = 1
stop ticks = 1

Sell Limit = 121
SL = 131
TP = 100
```

## Negative tests

- confirmed F2 must not arm;
- invalidated F2 must not arm;
- missing F1 waist must block;
- zero/negative geometry must block;
- current market beyond the intended limit must not become a market order;
- target touched before fill must cancel pending;
- second concurrent setup must not send;
- Hook construction must not exist in the fast detector;
- custom `Print` and CSV paths must not exist in the expert runtime.

## Required tester modes

1. `Every tick based on real ticks` for execution validation.
2. FAST profile for iteration.
3. PARITY profile for final structure comparison.
4. Visual spot-check of at least 20 bullish and 20 bearish setup paths.
