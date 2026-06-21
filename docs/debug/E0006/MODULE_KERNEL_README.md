# E0006 Modular Execution Kernel

This document describes the reusable modules extracted from the E0006 execution work. The goal is to stop rewriting the same structural ideas inside every EA and instead compose them from small, testable pieces.

## Why this layer exists

E0006 accumulated several independent ideas:

1. origin zones from M0001 structural nodes,
2. internal same-side hunt qualification,
3. optional revisit-only entries,
4. node-price versus zone-back stop anchoring,
5. pending-order and open-position side caps,
6. zero initial fixed-R TP with an internal opposite-node TP manager,
7. strict new-candle synchronization instead of tick-heavy computation.

Each idea is useful alone. A future executor may want only the internal-hunt filter, only the N-th opposite-node exit, or only the exposure caps. The new module layer breaks those ideas into reusable include files.

## Files

```text
mql5/Include/DecisionAlphaLab/Execution/E0006/DAL_E0006Types.mqh
mql5/Include/DecisionAlphaLab/Execution/E0006/DAL_E0006InternalHunts.mqh
mql5/Include/DecisionAlphaLab/Execution/E0006/DAL_E0006ZonePricing.mqh
mql5/Include/DecisionAlphaLab/Execution/E0006/DAL_E0006RevisitCycles.mqh
mql5/Include/DecisionAlphaLab/Execution/E0006/DAL_E0006ExitTargets.mqh
mql5/Include/DecisionAlphaLab/Execution/E0006/DAL_E0006ExposureCaps.mqh
mql5/Include/DecisionAlphaLab/Execution/E0006/DAL_E0006Modules.mqh
```

`DAL_E0006Modules.mqh` is the facade include. A new EA can include only that header and receive the full E0006 kernel.

## 1. Types and policies

File:

```text
DAL_E0006Types.mqh
```

This file defines shared contracts rather than behavior. It contains:

```text
DALE0006PricingPolicy
DALE0006InternalHuntPolicy
DALE0006RevisitPolicy
DALE0006ExitPolicy
DALE0006ExposurePolicy
DALE0006ZoneOrderPlan
```

The most important idea is that runtime inputs should be converted into policy structs once, then passed into reusable logic. That keeps future EAs clean.

Example:

```mql5
DALE0006PricingPolicy pricing;
DAL_E0006_DefaultPricingPolicy(pricing);
pricing.reward_r = InpRewardR;
pricing.stop_anchor = InpUseNodePriceStop ? DAL_E0006_STOP_NODE_PRICE : DAL_E0006_STOP_ZONE_BACK;
```

## 2. Internal hunt qualification

File:

```text
DAL_E0006InternalHunts.mqh
```

This module counts internal hunted nodes between an origin node and a decision point.

For a LOW origin, same-side mode means it counts internal LOW nodes only. For a HIGH origin, it counts internal HIGH nodes only.

Core functions:

```text
DAL_E0006_CountInternalHuntedNodesForOrigin(...)
DAL_E0006_CountInternalHuntedNodesBetween(...)
DAL_E0006_InternalHuntQualificationPassed(...)
```

This is the reusable version of the filter:

```text
minimum N same-side internal nodes must be hunted before the origin zone becomes eligible.
```

## 3. Zone pricing and stop anchoring

File:

```text
DAL_E0006ZonePricing.mqh
```

This module builds the executable price plan for a structural zone:

```text
entry
stop
optional fixed-R TP
risk distance
zone geometry
```

It uses M0001 territory logic for live zone geometry.

Supported stop modes:

```text
DAL_E0006_STOP_ZONE_BACK
DAL_E0006_STOP_NODE_PRICE
```

BUY rule:

```text
entry = LOW zone upper + spread multiplier
SL = zone lower or origin node price
```

SELL rule:

```text
entry = HIGH zone lower
SL = zone upper + spread, or origin node price + spread
```

Fixed-R TP is optional. If `reward_r = 0`, the plan has `tp = 0` so the later internal-node TP manager can own the exit.

## 4. Revisit-only cycle qualification

File:

```text
DAL_E0006RevisitCycles.mqh
```

This module lets a future executor require the first touch cycle and the revisit cycle to both satisfy the internal-hunt standard.

Conceptually:

```text
first touch must be clean: touched but not hunted
first cycle must have enough internal hunts
revisit cycle must also have enough internal hunts
only then can a revisit entry be considered valid
```

Core function:

```text
DAL_E0006_FirstAndRevisitCyclesQualified(...)
```

This makes the revisit-only idea reusable outside the current E0006 EA.

## 5. Internal opposite-node TP

File:

```text
DAL_E0006ExitTargets.mqh
```

This module finds the N-th opposite internal node after position entry.

BUY exit:

```text
N-th internal HIGH after entry
```

SELL exit:

```text
N-th internal LOW after entry
```

Core function:

```text
DAL_E0006_FindNthOppositeInternalNodeAfterEntry(...)
```

This lets future EAs use structure-defined exits without coupling themselves to the current E0006 order placement code.

## 6. Exposure caps

File:

```text
DAL_E0006ExposureCaps.mqh
```

This module isolates side-level exposure logic:

```text
count open BUY/SELL positions
block a side when open positions reach a threshold
delete managed pending orders from that side
```

Core functions:

```text
DAL_E0006_CountOpenPositionsByDirection(...)
DAL_E0006_SideBlockedByOpenCap(...)
DAL_E0006_DeletePendingOrdersByDirection(...)
```

## Suggested future migration

The current production EA can keep running as-is. The next clean refactor should gradually replace local functions with calls into the modules:

```text
E0006ZoneSetup                      -> DALE0006ZoneOrderPlan
E0006_BuildZoneSetup                -> DAL_E0006_BuildZoneOrderPlan + hunt/revisit filters
E0006_CountOpenPositionsByDirection -> DAL_E0006_CountOpenPositionsByDirection
E0006_FindNthOpposite...            -> DAL_E0006_FindNthOppositeInternalNodeAfterEntry
```

This should be done in small compile-safe releases rather than one giant rewrite.

## Design rule

The module layer should stay pure and composable:

```text
No global EA inputs
No chart objects
No heavy logging
No tick loop assumptions
No hidden dependence on a specific EA file
```

Inputs belong in the EA. Logic belongs in the modules.
