# M0001 Live Zone Resync

## Problem

The visible zone box must not freeze while the node is still alive.

Pending-touch/event geometry is intentionally frozen for exit-gap confirmation,
but the active live zone should continue to follow the latest expansion extreme.

## Fix

For every alive node:

```text
tracking_extreme updates on every new extension
territory_lower/upper are rebuilt from tracking_extreme
visible live zone uses the rebuilt territory
```

The pending event zone remains frozen internally for touch confirmation only:

```text
pending_touch_lower/upper = frozen event geometry
state.territory_lower/upper = current live territory while node is active
```

## Revisit cycles

After a confirmed revisit in HUNT mode:

```text
tracking_cycle_start = confirmation_index + 1
tracking_extreme = initial extreme from tracking_cycle_start
live zone starts at tracking_cycle_start_time
```

So the current live box does not stretch from the original node origin after a
confirmed revisit.

## Renderer safety

`DAL_DrawRectangle` now upserts geometry. If a rectangle already exists, both
anchor points are moved explicitly:

```text
ObjectMove(point 0, t1, upper)
ObjectMove(point 1, t2, lower)
```

This prevents stale rectangle coordinates if the same object name is reused.

## Version

`M0001_LiveVisualLab.mq5` version: `1.45`.
