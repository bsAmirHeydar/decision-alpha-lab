# E0006 — Exit, Stop, Spread, and Risk Logic

This document explains how E0006 places entries, anchors stops, handles spread, sizes risk, and manages take profit after a trade opens.

## Entry prices

E0006 uses limit orders on structural zones.

For LOW origin zones:

```text
BUY LIMIT entry = zone_upper + spread * InpBuyEntrySpreadMultiplier
```

The BUY entry is shifted upward because a buy fills on Ask. This adjustment is intentionally preserved even when stop mode changes.

For HIGH origin zones:

```text
SELL LIMIT entry = zone_lower
```

The SELL entry remains at the lower edge of the high/supply zone.

## Stop anchor modes

Input:

```text
InpUseNodePriceStop = false
```

There are two stop anchor modes.

### Zone-back stop mode

This is the original mode.

BUY / LOW origin:

```text
SL = zone_lower
```

SELL / HIGH origin:

```text
SL = zone_upper + spread * InpSellStopSpreadMultiplier
```

### Node-price stop mode

This mode uses the origin node price as the stop anchor.

BUY / LOW origin:

```text
SL = origin node price
```

SELL / HIGH origin:

```text
SL = origin node price + spread * InpSellStopSpreadMultiplier
```

The SELL stop receives the spread shift because a sell position is stopped by Ask crossing the stop. This matches the requested sell-side spread handling.

## Risk distance

After entry and stop are resolved, risk distance is:

```text
risk_distance = abs(entry - SL)
```

Risk sizing is calculated from:

```text
InpRiskCash
InpCommissionPerLotRoundTurn
InpAllowMinLotIfRiskTooSmall
```

If stop mode changes from zone-back to node-price, the risk distance changes, so position size changes too.

## Fixed-R TP

The current default is:

```text
InpRewardR = 0.0
```

Zero means pending orders are sent without an initial fixed-R take profit.

When fixed-R is enabled by setting `InpRewardR > 0`, TP is computed from the selected stop distance.

BUY:

```text
TP = entry + risk_distance * InpRewardR
```

SELL:

```text
TP = entry - risk_distance * InpRewardR + spread * InpSellTpSpreadMultiplier
```

The sell TP spread shift is used only in fixed-R TP mode.

## Internal opposite-node TP manager

The intended default exit is not fixed-R. It is internal-node based.

Inputs:

```text
InpUseInternalOppositeNodeTP = true
InpExitOppositeInternalNodeCount = 3
InpModifyPositionTPOnEveryNewBar = true
```

The manager runs once per new candle and updates open managed positions.

### BUY position exit

For a BUY opened from a LOW origin zone:

```text
count valid internal HIGH nodes after position entry
when count reaches InpExitOppositeInternalNodeCount
set TP at that internal HIGH price
```

Example with count 3:

```text
BUY opens
internal HIGH #1 becomes valid
internal HIGH #2 becomes valid
internal HIGH #3 becomes valid
TP is moved to HIGH #3 price
```

### SELL position exit

For a SELL opened from a HIGH origin zone:

```text
count valid internal LOW nodes after position entry
when count reaches InpExitOppositeInternalNodeCount
set TP at that internal LOW price
```

Example with count 3:

```text
SELL opens
internal LOW #1 becomes valid
internal LOW #2 becomes valid
internal LOW #3 becomes valid
TP is moved to LOW #3 price
```

## Why TP can be zero at order placement

Because the exit target depends on future internal nodes after the actual position entry, the target may not exist yet when the pending order is placed.

So the default order lifecycle is:

```text
pending limit placed with SL and TP=0
position opens
new candles create internal opposite nodes
N-th opposite node becomes valid
position TP is set or modified
```

The geometry checks were updated so TP=0 is accepted for pending orders while SL remains mandatory.

## Open-position side blocking

These inputs protect against over-stacking same-side exposure:

```text
InpMaxBuyOpenPositionsBeforeBlock = 0
InpMaxSellOpenPositionsBeforeBlock = 0
InpDeleteSidePendingWhenOpenCapHit = true
```

If a side reaches its open-position threshold, E0006 deletes managed pending orders of that side and stops placing new pending orders of that side during the sync.

Example:

```text
InpMaxBuyOpenPositionsBeforeBlock = 2
```

When two managed BUY positions are already open, all managed BUY LIMIT orders are deleted and no new BUY LIMIT order is placed. SELL remains independent.

## Per-side pending caps

These inputs cap pending orders even before positions open:

```text
InpMaxBuyPendingOrders = 0
InpMaxSellPendingOrders = 0
```

`0` means unlimited.

When a positive cap is set, E0006 keeps the newest eligible zones first and lets stale cleanup delete older extra pending orders.

## Recommended risk/exit profiles

Pure internal-node exit:

```text
InpRewardR = 0.0
InpUseInternalOppositeNodeTP = true
InpExitOppositeInternalNodeCount = 3
```

Fixed-R test:

```text
InpRewardR = 20.0
InpUseInternalOppositeNodeTP = false
```

Hybrid safety test:

```text
InpRewardR = 20.0
InpUseInternalOppositeNodeTP = true
InpExitOppositeInternalNodeCount = 3
```

In hybrid mode, the pending order starts with fixed-R TP, and the internal-node manager can later modify the TP when the N-th opposite internal node appears.
