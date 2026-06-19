# M0001 Consumed Zone History

## Rule

When a node is consumed, the live decision process is finished, but the historical
hunt/territory rectangle should remain visible on the chart up to the consume
candle.

## Behavior

Active node:

```text
zone_start = node_time
zone_end   = current live-stream bar
```

Consumed node:

```text
zone_start = node_time
zone_end   = consumed_time
```

The zone does not extend after consumption.

## Input

```text
InpShowConsumedHuntZoneHistory = true
```

Set it to `false` to hide consumed zones completely.

## Important

Expansion extreme remains a live variable only while the node is active. The zone
history is kept for visual audit, not because the node remains active.

Version: `1.23`.
