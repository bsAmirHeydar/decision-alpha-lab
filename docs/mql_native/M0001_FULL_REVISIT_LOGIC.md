# M0001 Full Revisit Logic

## Revisit definition

A revisit is a completed territory interaction event for a node that has not yet
been consumed.

```text
TRACKING -> PENDING REV#n -> TOUCH_CONFIRMED REV#n -> TRACKING -> PENDING REV#n+1
```

## Start condition

A revisit starts when a candle intersects the current live territory zone:

```text
bar.low <= territory_upper && bar.high >= territory_lower
```

At this exact entry candle, event geometry freezes:

```text
event_extreme = tracking_extreme
event_lower   = live_lower
event_upper   = live_upper
```

## Active event

While the event is active:

```text
event_lower/event_upper stay frozen
tracking_extreme keeps updating for future revisits
```

This prevents the current revisit from repainting, while still keeping the node's
future territory correct if the node remains alive.

## Touch confirmation

A pending touch becomes confirmed only after:

```text
outside_count >= exit_gap
```

using the frozen event zone.

## HUNT priority

HUNT always has priority before touch confirmation:

```text
LOW node  -> bar.low  < node_price
HIGH node -> bar.high > node_price
```

If this happens during a pending revisit, that revisit closes as HUNT and the node
is consumed by HUNT.

## Consumption modes

TOUCH mode:

```text
REV#0 starts
if HUNT before confirmation -> CONSUMED:HUNT
if exit_gap confirms touch  -> CONSUMED:TOUCH
no REV#1
```

HUNT mode:

```text
REV#0 confirms -> node remains active
REV#1 confirms -> node remains active
...
HUNT -> CONSUMED:HUNT
```

## Visuals

New visual inputs:

```text
InpShowRevisitLabels = true
InpShowNodeStateLabels = true
```

Labels:

```text
REV#0 TOUCH_OK len=...
REV#1 HUNT CONSUMED:HUNT len=...
PENDING REV#2 out=3/6
TRACKING nextREV#2 confirmed=2
CONSUMED:TOUCH revs=1
CONSUMED:HUNT revs=3
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.40`.
