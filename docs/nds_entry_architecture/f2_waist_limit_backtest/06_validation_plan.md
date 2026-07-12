# F2 Waist Limit — Validation Plan

## Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

## Positive cases

1. Newly observable bullish F2 creates a Buy Limit below F2 waist.
2. Newly observable bearish F2 creates a Sell Limit above F2 waist.
3. Request carries F1-waist SL and F2-Leg2 TP.
4. `OrderCheck` and `OrderSend` accept the request.
5. Pending order blocks later detector runs.
6. Filled position blocks later detector runs.
7. After broker SL/TP closes exposure, a later fresh F2 may trade.

## Critical freshness case

The F2 confirmation pivot time is not the setup availability time. Confirmed swing nodes require right-side L clearance. The setup age must therefore be measured from the exact bar where that clearance became complete.

Test with L=2, L=3 and equal-price touches on the right side. Equal touches must not advance clearance.

## Negative cases

- unconfirmed F2;
- missing F1 parent waist;
- stale availability bar;
- reused structural setup;
- wrong Entry/SL/TP ordering;
- pending price on wrong side of Bid/Ask;
- broker distance violation;
- invalid volume;
- foreign position on the same symbol;
- more than one managed exposure.
