# E0006 — Structural Execution Layer Overview

E0006 is the execution-facing layer of Decision Alpha Lab. It does **not** try to discover an alpha by itself and it does **not** redefine the structural market logic. Its job is to translate already-defined structural zones and internal-node conditions into managed limit orders, position-side caps, stop placement, and take-profit management.

The module is intentionally built as a thin executor around the existing modules:

- M0001 supplies the live territory/zone semantics, touch/revisit events, node hunt state, and node invalidation logic.
- the L-rule structural node engine supplies confirmed origin nodes and confirmed internal nodes.
- the execution helpers supply spread-aware price normalization, order placement, stale-order deletion, and risk sizing.

E0006 therefore has one main contract:

```text
structural source of truth = existing modules
execution responsibility   = order lifecycle around those structures
```

## High-level cycle

E0006 runs once per new candle. It is not designed as a tick-by-tick scanner.

On each sync:

```text
1. load closed bars
2. detect origin nodes with InpOriginNodeL
3. detect internal game nodes with InpInternalNodeL
4. compute M0001 origin events when revisit-only mode needs them
5. update TP of already-open managed positions
6. count open positions per side
7. block/delete side pending orders if open-position caps are reached
8. scan newest origin zones first
9. build one setup per valid origin zone
10. apply entry qualification filters
11. respect per-side pending caps
12. upsert managed limit orders
13. delete stale managed pending orders
```

The newest-origin-first scan is deliberate. When a cap is active, newer structures win over older structures.

## Two structural scales

E0006 separates the structure that receives the order from the structure that qualifies the order.

```text
InpOriginNodeL   = L for the origin node whose zone gets the limit order
InpInternalNodeL = L for smaller/internal nodes used for entry filters and exit targets
```

This matters because the tradeable zone may be a higher-level structure, while the confirmation of pressure, sweep, or path behavior may be better measured at a smaller structural scale.

## Origin zone

An origin zone is the zone of a confirmed node detected with `InpOriginNodeL`.

LOW origin:

```text
potential BUY LIMIT zone
```

HIGH origin:

```text
potential SELL LIMIT zone
```

The zone geometry comes from live M0001 territory semantics. E0006 does not create a separate private zone model.

## Internal game

Internal nodes are detected separately with `InpInternalNodeL` and are used for two things:

```text
1. entry qualification
2. take-profit placement after position entry
```

For entry qualification, same-side internal hunts can be required:

```text
LOW origin  -> count hunted internal LOW nodes
HIGH origin -> count hunted internal HIGH nodes
```

For exits, opposite internal nodes are counted:

```text
BUY position  -> count valid internal HIGH nodes after entry
SELL position -> count valid internal LOW nodes after entry
```

## Managed order identity

E0006 builds comments through the managed execution comment prefix. This makes each pending order trackable by symbol, magic number, and managed comment. The stale-order cleanup only acts on managed orders matching this prefix and magic number.

That separation is important: the EA should not accidentally delete unrelated manual orders or unrelated EA orders.

## Main execution modes

E0006 currently supports these major modes:

```text
standard all-zone mode
per-side pending caps
open-position side blocking
internal same-side hunt qualification
optional revisit-only entry
internal opposite-node TP management
zone-back or node-price stop anchors
```

These modes are independent enough to be tested in isolation, but in the full intended configuration they form a structural execution lifecycle:

```text
origin zone exists
-> internal same-side pressure/hunt proves the path
-> optional revisit cycle proves the zone has survived a first touch
-> limit order waits at the zone edge
-> stop is placed behind zone or node
-> open position exits at the N-th opposite internal node
```

## Current recommended baseline

A clean structural test configuration is:

```text
InpOriginNodeL = 5
InpInternalNodeL = 2
InpZoneRatio = 0.90

InpUseInternalHuntFilter = true
InpMinInternalHuntsForZone = 3
InpInternalHuntSameSideOnly = true

InpOnlyTradeRevisitZones = false

InpRewardR = 0.0
InpUseInternalOppositeNodeTP = true
InpExitOppositeInternalNodeCount = 3

InpUseNodePriceStop = false

InpUpdateEveryNBars = 1
InpPrintOrderLogs = false
```

For a stricter retest-only experiment:

```text
InpOnlyTradeRevisitZones = true
InpRevisitFirstCycleMustQualify = true
InpRevisitMinInternalHunts = 0
```

`InpRevisitMinInternalHunts = 0` means reuse `InpMinInternalHuntsForZone`.

## Compile target

```text
mql5/Experts/DecisionAlphaLab/Execution/E0006_AllZoneTouchLimitFixedR.mq5
```
