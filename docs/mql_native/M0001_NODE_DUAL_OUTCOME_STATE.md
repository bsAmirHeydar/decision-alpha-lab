# M0001 Node Dual Outcome State

## Purpose

Every node now stores TOUCH and HUNT information independently of the selected
consumption model.

The consumption model only decides when a node becomes inactive.

## Stored on each audit state

```text
touch_started
first_touch_time
touch_confirmed
touch_confirmed_time
hunted
hunt_time
consumed
consumed_time
consume_reason
```

## Logic

A zone touch starts only a pending touch event:

```text
zone touch -> touch_started=true
```

The touch is confirmed only if the event exits cleanly:

```text
outside_count >= InpExitGap -> touch_confirmed=true
```

If the node breaks before touch confirmation:

```text
LOW  node: bar.low  < node_price -> hunted=true
HIGH node: bar.high > node_price -> hunted=true
```

That outcome becomes HUNT.

## Consumption model

In TOUCH mode:

```text
confirmed touch -> consumed by TOUCH
hunt before confirmation -> consumed by HUNT
```

In HUNT mode:

```text
confirmed touch -> stored only, node remains active
hunt -> consumed by HUNT
```

Once a node is consumed, no further candles are scanned for that node.

## Journal

When `InpWriteValidationJournal=true`, a new file is written:

```text
<symbol>_M0001_node_audit_states.csv
```

This file stores the node-level touch/hunt/consume state.

## Version

`M0001_LiveVisualLab.mq5` version: `1.32`.
