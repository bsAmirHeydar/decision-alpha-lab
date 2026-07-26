# H6 Fast Box Visualizer — Official Algorithm

## Source of truth

H6 does not compute touch, extreme, zone, revisit, or invalidation. It uses M0001 only:

- `DAL_DetectLRuleNodes`
- `DAL_M0001ComputeEvents`
- `event.territory_lower`
- `event.territory_upper`
- `event.entry_index`
- `event.exit_index`
- `event.touch_confirmed`

## What gets drawn

By default, every confirmed M0001 event gets exactly one persistent box.

This is intentionally broader than the old horizon-only logic so no touched/revisited event disappears just because it is below H1.

## Geometry

Box vertical bounds are exactly M0001 territory:

```text
lower = event.territory_lower
upper = event.territory_upper
```

H6 does not rebuild zone geometry.

## Time range

Default:

```text
left  = event.entry_time
right = event.exit_time
```

`InpH6BoxRightMode`:

- `0`: right edge = horizon candle
- `1`: right edge = M0001 event exit candle
- `2`: right edge = latest available bar

## Color

Touch candle is zero. Age is:

```text
age = event.exit_index - event.entry_index
```

Color:

```text
age < H1       -> pre-horizon color
age >= H1      -> red
age >= H2      -> green
age >= H3      -> purple
```

## Persistence

Boxes use this prefix:

```text
DAL_H6_PERSIST_BOX_
```

Live updates never delete boxes. Lifecycle is upsert-only:

```text
missing box  -> ObjectCreate
existing box -> ObjectMove/ObjectSetInteger color only
```

## Execution

H6 runs:

- once on init for backfill
- once per new candle for live update

It never runs per tick.

## Performance

No heavy journal printing by default:

```text
InpH6PrintAudit = false
```

No lines, markers, circles, levels, or debug objects are created.


Release 137 time-origin fix:
- Box horizontal origin is exactly the original node candle time: `event.node_time`.
- Box horizontal destination is exactly the first M0001 touch/revisit candle time: `event.entry_time`.
- This includes wick/shadow-only touches because M0001 entry is based on candle range intersecting the frozen territory.
- H6 no longer uses horizon, exit, or latest-bar time as the rectangle right edge.
- `InpH6BoxRightMode` was removed; the time policy is fixed and official.


Release 138 color update fix:
- Box color age is now based on `event.rtv_sample_length - 1`.
- This matches the official candle count: the touch candle is zero and M0001 exit-gap candles are not counted.
- Existing box colors are monotonic by default: pre -> red -> green -> purple.
- A persistent box never downgrades color during later live windows or partial recalculations.
- `InpH6NeverDowngradeBoxColor=true` controls this behavior.


Release 139 dynamic color tracking:
- H6 box color no longer depends on `event.rtv_sample_length` or `event.exit_index`.
- After a confirmed M0001 touch/revisit creates a box, H6 checks every closed candle after entry.
- Color tracking stops only when the far/back side of the frozen M0001 territory is hit or the purple/highest horizon is reached.
- HIGH node back side = `event.territory_upper`; LOW node back side = `event.territory_lower`.
- The touch candle is zero; the first closed candle after touch is one.
- Persistent box names no longer include `revisit_id`, so the same node/touch box updates reliably across live windows.
- Official default is closed-candle only: `InpH6IncludeLiveBar=false`.


Release 140 valid-zone color lifecycle:
- Zone-back hit before the max/purple horizon invalidates the box.
- If an orange/red/green box already existed and the zone back is hit before purple, it is deleted/hidden because the zone no longer has value.
- If purple is reached before any zone-back hit, the box is considered completed and remains purple; later zone-back hits are not tracked.
- Colors are visible only while the frozen M0001 territory back side has not been hit.
- New input: `InpH6InvalidateOnZoneBackHitBeforeMax=true`.


## Release 141 — selectable zone projection mode

H6 can now draw and age the same M0001 event map with two visual/validity projections.

### `DAL_M0006_ZONE_FULL_M0001_TERRITORY`

This is the previous behavior.

- Box lower/upper = frozen M0001 `territory_lower` / `territory_upper`.
- Back-hit invalidation uses the far/back side of that full territory.
- Existing object names are preserved.

### `DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE`

This is the new node-capped map requested for studying near-node reactions.

- LOW node: projected box = `[node_price, territory_upper]`.
- HIGH node: projected box = `[territory_lower, node_price]`.
- The back/invalid side is the exact node price.
- If high/low hits the node price, the box is invalid and is deleted/hidden before max horizon.
- With `InpH6NodeCappedInvalidateOnTouchCandle=true`, a touch candle that already hits the node price creates no meaningful box.

This mode isolates cases where price reaches the inner/90-percent zone edge but does **not** hit the node itself. In visual terms, the old territory is effectively reduced to the node-capped half that lies between the reaction edge and the exact node price.

Important: when switching visual projection modes on an already-used chart, use `InpH6ClearPersistentBoxesOnInit=true` once if old boxes should be removed from the chart.
