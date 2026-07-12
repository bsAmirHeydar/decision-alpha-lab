# F2 Waist Limit — Price Semantics

## Canonical references

- `F2 waist`: `FP_FlagEvent.waist.price` on the confirmed F2.
- `F1 waist`: `FP_FlagEvent.waist.price` on the canonical parent F1.
- `F2 leg end`: `FP_FlagEvent.leg2.price` after the existing pre-internal extension absorption pass.

## Entry

The phrase “under the F2 waist” is implemented directionally:

- Bullish F2: one configurable point below the F2 waist.
- Bearish F2: the mirrored location, one configurable point above the F2 waist.

No market-order fallback exists. If the resulting level is not a legal pending limit relative to current Bid/Ask and broker freeze/stops levels, the setup is blocked.

## Stop

The Stop is the exact F1 waist, with tick-size normalization only. No ATR, spread buffer, point padding or hidden widening is applied.

## Target

The Take Profit is the exact current F2 Leg2 endpoint, with tick-size normalization only. There is no R-multiple target and no F3 exit in this profile.

## Closed-bar authority

F2 confirmation must exist in the closed-bar detector output. Live-bar pending nodes are disabled by default.
