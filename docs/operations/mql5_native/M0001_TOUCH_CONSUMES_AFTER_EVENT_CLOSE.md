# M0001 Touch Mode: Consume After Event Completion

## Decision

Touch mode now follows the README semantics:

```text
first territory-zone touch -> first event starts
first event completes       -> node is consumed
```

Touch does **not** consume the node immediately.

## Event completion

An event is complete when price has stayed outside the frozen event territory for
`exit_gap` consecutive candles.

```text
outside_count >= exit_gap
```

## Frozen event geometry

When the first touch starts an event:

```text
event_extreme = current expansion extreme
event_lower   = current territory lower
event_upper   = current territory upper
```

These are frozen for the event. They are not updated while the event is active.

## HUNT mode

Hunt mode remains separate:

```text
LOW node  consumed when bar.low  < node_price
HIGH node consumed when bar.high > node_price
```

Zone touches in hunt mode start/revisit events, but do not consume the node unless
the node price is broken.

## Why this matters

This preserves revisit semantics:

```text
TOUCH mode -> one completed event, then consumed
HUNT mode  -> multiple revisits are possible until node break
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.30`.
