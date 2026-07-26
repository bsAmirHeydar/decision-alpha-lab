# M0001 Node-Origin Zones and Revisit Text Colors

## Zone visual origin

The live zone rectangle must start from the structural node candle:

```text
rectangle_start_time = node_time
```

This is a visual rule only.

The post-revisit calculation cycle still uses:

```text
tracking_cycle_start = confirmation_index + 1
```

So after a confirmed revisit in HUNT mode:

```text
price geometry = based on post-visit reset extreme
time origin    = still drawn from the original node candle
```

This keeps the chart visually anchored to the real structural node while the
zone's price limits still update from the current reset extreme cycle.

## Revisit text colors

Actual revisit labels remain clean:

```text
REVISIT#1
REVISIT#2
```

The text color now indicates node side:

```text
LOW / valley revisit  -> blue
HIGH / peak revisit   -> red
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.46`.
