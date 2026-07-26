# E0006 — Entry Qualification Logic

This document describes how E0006 decides whether a structural zone is allowed to receive a limit order.

The entry decision is not simply “every zone gets an order.” The current executor can require the path after the origin node to prove that enough same-side internal nodes were hunted before the origin zone becomes tradeable.

## Origin versus internal nodes

E0006 uses two L values.

```text
InpOriginNodeL   = L for the main zone node
InpInternalNodeL = L for the internal nodes used as path evidence
```

The origin node is the anchor of the trade. The internal nodes are the evidence that price has created and hunted enough same-side liquidity before the order is allowed.

## Standard same-side hunt filter

Inputs:

```text
InpUseInternalHuntFilter = true
InpMinInternalHuntsForZone = 3
InpInternalHuntSameSideOnly = true
```

With this setup, a zone is not eligible until at least three same-side internal nodes have been hunted after the origin node.

## LOW origin / BUY logic

For a LOW origin, E0006 is considering a BUY LIMIT.

The same-side internal nodes are internal LOW nodes.

```text
origin = LOW node
order  = BUY LIMIT
internal evidence = hunted internal LOW nodes after origin
```

A LOW origin zone becomes eligible only when:

```text
count(hunted internal LOW nodes after origin) >= InpMinInternalHuntsForZone
```

Example with threshold 3:

```text
LOW origin forms
internal LOW #1 forms and is hunted
internal LOW #2 forms and is hunted
internal LOW #3 forms and is hunted
LOW origin zone becomes orderable
```

The order is still placed at the configured zone edge, not at the internal node.

## HIGH origin / SELL logic

For a HIGH origin, E0006 is considering a SELL LIMIT.

The same-side internal nodes are internal HIGH nodes.

```text
origin = HIGH node
order  = SELL LIMIT
internal evidence = hunted internal HIGH nodes after origin
```

A HIGH origin zone becomes eligible only when:

```text
count(hunted internal HIGH nodes after origin) >= InpMinInternalHuntsForZone
```

Example with threshold 3:

```text
HIGH origin forms
internal HIGH #1 forms and is hunted
internal HIGH #2 forms and is hunted
internal HIGH #3 forms and is hunted
HIGH origin zone becomes orderable
```

## Hunt definition

Internal hunt detection uses the existing project predicate:

```text
DAL_M0001Hunted(...)
```

E0006 does not invent a new private definition of hunt. That keeps the execution layer aligned with the structural hypothesis layer.

For LOW internal nodes, a hunt means the internal low is broken according to the M0001 hunt predicate.

For HIGH internal nodes, a hunt means the internal high is broken according to the same predicate.

## Decision window

The standard filter counts internal hunted nodes after the origin node and before the current decision point.

Because E0006 is new-bar-only, the decision point is the latest closed candle available in the sync pass.

```text
origin index + 1  -> latest closed candle
```

## Same-side toggle

If this is true:

```text
InpInternalHuntSameSideOnly = true
```

then:

```text
LOW origin  -> only internal LOW hunts count
HIGH origin -> only internal HIGH hunts count
```

If it is false, the filter can count both sides. The current intended experiment is same-side only.

## Interaction with pending caps

Entry qualification happens before per-side pending caps.

The order of filtering is:

```text
1. origin zone valid and not hunted
2. entry qualification passed
3. side not blocked by open-position count
4. per-side pending cap not exceeded
5. limit order upserted
```

This means a rejected zone does not consume one of the side cap slots.

## Fast test settings

To quickly verify that the filter is actually controlling order generation:

```text
InpMinInternalHuntsForZone = 1
InpPrintOrderLogs = true
```

Then raise it back to the intended threshold:

```text
InpMinInternalHuntsForZone = 3
```
