# F2 Waist Limit — Price Semantics

## Structural references

- Entry reference: confirmed F2 `waist.price`.
- Stop reference: canonical same-direction parent F1 `waist.price`.
- Target reference: confirmed F2 `leg2.price` after Phoenix extension absorption.

## Tick semantics

The offset is expressed in symbol trade ticks, not generic points:

```text
Bullish entry = floor-to-tick(F2 waist − offset ticks)
Bearish entry = ceil-to-tick(F2 waist + offset ticks)
```

F1 waist and F2 Leg2 are normalized to the nearest valid trade tick. No ATR, spread padding, hidden widening, fixed-R target or market-order fallback is applied.

## Broker legality

The exact structure must also satisfy:

- Buy Limit below current Ask by the symbol stop-distance requirement.
- Sell Limit above current Bid by the symbol stop-distance requirement.
- SL and TP on the correct side of entry.
- Entry-to-SL and entry-to-TP distances not below `SYMBOL_TRADE_STOPS_LEVEL`.
