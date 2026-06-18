# M0001 Node Dual Outcome State

Version: active semantics preserved in 1.59

## Purpose

Every node stores TOUCH and HUNT information independently of the selected consumption model. The consumption model decides when a node becomes inactive.

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
pending_touch
pending_touch_revisit_id
confirmed_touch_count
next_revisit_id
revisited_live
fresh_live
```

## Logic

A zone touch starts only a pending touch event:

```text
zone touch -> pending_touch=true
```

The touch is confirmed only after strict exit-gap closure:

```text
outside_count >= InpExitGap -> touch_confirmed=true
```

If the node price breaks before touch confirmation:

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
confirmed touch -> stored as node memory, node remains active
hunt -> consumed by HUNT
```

Once a node is consumed, no further candles are scanned for that node.

## Reporting

The old validation-journal CSV writer is retired. Current audit state is used for final chart drawings and final compact node-vs-random logRTV reports.
