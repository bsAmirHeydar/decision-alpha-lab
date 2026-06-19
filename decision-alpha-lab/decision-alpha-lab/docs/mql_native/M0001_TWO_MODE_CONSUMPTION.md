# M0001 Two-Mode Node Consumption

## Purpose

M0001 node consumption is now explicit and two-mode:

```text
HUNT_NODE_BREAK
TOUCH_ZONE
```

## Inputs

```text
InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT
```

or:

```text
InpConsumeMode = DAL_M0001_CONSUME_BY_TOUCH
```

Legacy alias is kept:

```text
InpConsumeOnTouch = true
```

If `InpConsumeOnTouch=true`, it forces touch-zone mode.

## Mode 1: hunt / node break

```text
LOW node consumed when bar.low < node_price
HIGH node consumed when bar.high > node_price
```

Zone touches do not consume the node. The node remains active until its actual
price level is broken.

## Mode 2: touch zone

The node is consumed on the first candle that intersects its current territory
zone.

```text
touch = candle high/low intersects territory_lower/territory_upper
```

When consumed by touch, the audit extreme and zone history are frozen at the touch
candle. They remain visible as history but do not keep updating.

## Underlying code changes

This is not just a visual change.

`DAL_M0001ComputeNodeAuditStates()` now applies the selected consume mode while
tracking each node live.

`DAL_M0001ComputeEvents()` also records consumed state, consumed index/time, and
consume reason for event journals.

## Visual change

Consumed markers now show:

```text
CONSUMED:TOUCH
CONSUMED:HUNT
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.29`.
