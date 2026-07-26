# E0006 — Revisit Secondary-Node Entry and Stop Anchors

This document defines the third stop-anchor mode and the second revisit-entry mode added after the original E0006 execution design.

## Why this mode exists

In the first E0006 revisit model, the origin node stays the main execution anchor:

```text
origin node -> first touch without hunt -> later revisit -> enter again at origin zone
```

The new model treats the first touch as a structural event that can create a smaller same-side node. On the next revisit, execution can be transferred from the large origin node to this smaller node.

For a BUY example:

```text
large LOW origin is touched
origin is not hunted
inside that first touch cycle, a smaller valid LOW appears
later price revisits
entry can now be placed in the smaller LOW zone
SL can be placed below the smaller LOW node
```

For SELL, the logic is symmetric with HIGH nodes.

## Inputs

```text
InpOnlyTradeRevisitZones = true
InpRevisitEntryAnchorMode = E0006_REVISIT_ENTRY_ORIGIN_ZONE
InpStopAnchorMode = E0006_STOP_ORIGIN_ZONE_BACK
```

Available revisit entry anchors:

```text
E0006_REVISIT_ENTRY_ORIGIN_ZONE
E0006_REVISIT_ENTRY_SECONDARY_NODE_ZONE
```

Available stop anchors:

```text
E0006_STOP_ORIGIN_ZONE_BACK
E0006_STOP_ORIGIN_NODE
E0006_STOP_REVISIT_SECONDARY_NODE
```

The secondary-node modes require `InpOnlyTradeRevisitZones = true` because there is no first-touch secondary node before the first touch exists.

## Revisit entry mode 1 — origin zone

This is the original revisit behavior.

For BUY:

```text
entry = origin LOW zone upper + spread
```

For SELL:

```text
entry = origin HIGH zone lower
```

The first non-hunted touch is only a qualification event. The later order still belongs to the origin zone.

## Revisit entry mode 2 — secondary-node zone

This is the new behavior.

E0006 finds the same-side internal node whose pivot was created inside the first non-hunted touch cycle.

For BUY:

```text
origin = LOW
secondary node = same-side internal LOW created during first touch cycle
entry = secondary LOW zone upper + spread
```

For SELL:

```text
origin = HIGH
secondary node = same-side internal HIGH created during first touch cycle
entry = secondary HIGH zone lower
```

If multiple same-side internal nodes exist inside the first touch cycle, E0006 chooses the more extreme one:

```text
BUY / LOW  -> lowest internal LOW
SELL / HIGH -> highest internal HIGH
```

The secondary node must still be valid. If it has already been hunted, the setup is rejected.

## Stop mode 1 — origin zone back

```text
InpStopAnchorMode = E0006_STOP_ORIGIN_ZONE_BACK
```

BUY:

```text
SL = origin zone lower
```

SELL:

```text
SL = origin zone upper + spread
```

## Stop mode 2 — origin node

```text
InpStopAnchorMode = E0006_STOP_ORIGIN_NODE
```

BUY:

```text
SL = origin LOW node price
```

SELL:

```text
SL = origin HIGH node price + spread
```

## Stop mode 3 — revisit secondary node

```text
InpStopAnchorMode = E0006_STOP_REVISIT_SECONDARY_NODE
```

This mode only makes sense in revisit mode.

BUY:

```text
SL = secondary LOW node price
```

SELL:

```text
SL = secondary HIGH node price + spread
```

The sell stop always receives spread because the short stop is triggered by Ask.

## Recommended secondary-node revisit experiment

```text
InpOnlyTradeRevisitZones = true
InpRevisitEntryAnchorMode = E0006_REVISIT_ENTRY_SECONDARY_NODE_ZONE
InpStopAnchorMode = E0006_STOP_REVISIT_SECONDARY_NODE

InpOriginNodeL = 5
InpInternalNodeL = 2
InpMinInternalHuntsForZone = 3
InpRevisitFirstCycleMustQualify = true
InpRevisitMinInternalHunts = 0
```

This means:

```text
large origin node defines the first structural area
first touch must be non-hunted and qualified
same-side internal node created during first touch becomes the new execution anchor
later revisit order is placed at the secondary node zone
stop is placed behind the secondary node
```
