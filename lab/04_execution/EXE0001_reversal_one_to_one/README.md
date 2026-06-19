# EXE0001 — H0005 Reversal Fixed-R Touch Executor

## Purpose

Execute the reversal side of Hypothesis 5 as directly as possible in live/Strategy Tester conditions.

This module does not invent a new strategy. It converts the research event into pending-limit execution:

```text
H0005 reversal regime
next structural node zone touch
limit entry at first touch edge
stop behind the zone
fixed reward multiple, default 1R
```

## Build

```text
E0001_ReversalOneToOne.mq5 build 1.13
```

## Inputs that define the contract

```text
InpRewardR = 1.0
InpBuyLimitSlots = 0
InpSellLimitSlots = 0
InpMaxSimultaneousTrades = -1
InpAllowOppositeTrades = true
InpAllowMarketCatchWhenAlreadyTouching = false
InpCancelManagedPendingsAfterEntry = false
InpRefreshSetupsOnNewBarOnly = false
InpManageOrdersEveryTick = true
```

`InpBuyLimitSlots = 0` and `InpSellLimitSlots = 0` mean unlimited active touch limits. Positive values are optional safety caps.

## Entry and stop geometry

For `zone_ratio = 0.90`, the zone is the 10% territory band around the node.

### Buy limit from LOW node

```text
entry = zone_upper + spread
SL    = zone_lower
risk  = entry - SL
TP    = entry + risk * InpRewardR
```

### Sell limit from HIGH node

```text
entry = zone_lower
SL    = zone_upper + spread
risk  = SL - entry
TP    = entry - risk * InpRewardR
```

## Revisit behavior

The EA allows repeated trades on the same node only when they are true revisits:

```text
fill once for the current touch
lock that node comment
unlock only after price leaves the touch edge by InpTouchRevisitResetBufferPoints
place again on the next revisit while the node remains unconsumed
```

## Consumption

A simple historical touch does not retire the node. A structural hunt/consumption does. Once consumed, the node is no longer used.

## Continuation regime

If the latest regime is continuation/non-reversal, all managed pending orders are deleted. Open positions are not force-closed.

## Debug report

Use verbose logs when validating:

```text
InpLogMode = DAL_EXEC_LOG_VERBOSE
```

Expected journal tags:

```text
DAL_E0001_BUILD_SANITY
DAL_E0001_CACHE
DAL_E0001_LIMIT_ORDER
DAL_E0001_PENDING_UPDATE
DAL_E0001_PENDING_DELETE
DAL_E0001_TOUCH_LOCK
DAL_E0001_TOUCH_UNLOCK
DAL_E0001_CYCLE
```
