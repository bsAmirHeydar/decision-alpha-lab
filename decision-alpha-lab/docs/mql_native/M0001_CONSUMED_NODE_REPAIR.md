# M0001 Consumed Node Repair

## Rule

Once a node is consumed/hunted, its job is finished.

For a consumed node:

```text
active = false
extreme line = not drawn
live hunt zone = not drawn
```

The expansion extreme is a live decision variable only while the node is still
active.

## Engine change

`DAL_M0001ComputeNodeAuditStates()` now stops scanning a node immediately when it
is consumed/hunted. It does not continue updating the expansion extreme after the
consume candle.

## Visual change

Active nodes can show:

```text
node -> expansion extreme line
live hunt/territory zone
```

Consumed nodes show only an optional marker:

```text
InpShowConsumedNodeMarkers = true
```

## Important

The structural node remains on the chart for audit history, but the active extreme
and live hunt zone disappear after consumption.

Version: `1.22`.
