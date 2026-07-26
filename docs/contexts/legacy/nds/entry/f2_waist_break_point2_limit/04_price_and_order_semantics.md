# 04 — Price and Order Semantics

## Entry

Entry must be strictly beyond the F2 waist.

```text
Bullish: entry = F2 Waist - N trade ticks
Bearish: entry = F2 Waist + N trade ticks
```

`N` is configurable but clamped to at least one trade tick. Zero does not satisfy the Point-2 contract because equality with the waist is Point 1, not a strict waist break.

## Stop

Stop must be strictly beyond the direct parent F1 waist.

```text
Bullish: stop = F1 Waist - M trade ticks
Bearish: stop = F1 Waist + M trade ticks
```

`M` is configurable but clamped to at least one trade tick.

## Target

```text
target = F2 Leg2 price
```

This is the endpoint of the two-leg F2 flag. It is not:

- `f2.confirm`;
- an F3 endpoint;
- a fixed R multiple;
- the latest Hook extreme.

## Broker geometry

Orders are submitted only when:

```text
Bullish: stop < entry < target and entry < Ask
Bearish: target < entry < stop and entry > Bid
```

The broker's minimum stop-distance contract is also enforced.

## Missed-order policy

If the market is already beyond the intended limit when the body becomes observable, the setup is skipped. It is never converted into a market order.

## Target-consumption policy

If the target is touched while the pending order still exists, the pending is cancelled because the intended continuation path has already completed without producing Point-2 entry.
