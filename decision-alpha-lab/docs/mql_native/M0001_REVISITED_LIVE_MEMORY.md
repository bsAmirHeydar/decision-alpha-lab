# M0001 Revisited Live Memory

## Core idea

A revisit does not have to happen immediately after the previous event.

In HUNT consumption mode, a confirmed touch does not kill the node. The node
returns to normal tracking and can be revisited much later.

```text
unconsumed node = live node
unconsumed revisited node = live node + memory
```

## Fresh live node

A node is fresh while it is alive and has no confirmed revisit:

```text
fresh_live = true
confirmed_touch_count = 0
next_revisit_id = 0
```

Visual label:

```text
FRESH LIVE next=REV#0
```

In TOUCH mode:

```text
FRESH LIVE TOUCH_EVENT
```

## Pending revisit

When price enters the live territory zone, the next revisit starts:

```text
pending_touch = true
pending_touch_revisit_id = next_revisit_id
```

Visual label:

```text
PENDING REV#N out=x/exit_gap
```

In TOUCH mode:

```text
PENDING TOUCH_EVENT out=x/exit_gap
```

## Confirmed revisit

A pending revisit becomes confirmed only after:

```text
outside_count >= exit_gap
```

In HUNT mode, confirmation stores memory and returns the node to tracking:

```text
confirmed_touch_count += 1
next_revisit_id += 1
state = REVISITED LIVE
```

The next revisit can happen many candles later.

Visual label:

```text
REVISITED LIVE revs=N next=REV#N age=B
```

`age` is the number of bars since the last confirmed revisit.

## Consumption

In TOUCH mode:

```text
first confirmed touch -> CONSUMED:TOUCH
hunt before confirmation -> CONSUMED:HUNT
```

There is no true multi-revisit loop in TOUCH mode.

In HUNT mode:

```text
confirmed revisit -> memory only
node break -> CONSUMED:HUNT
```

The consumed label keeps the number of confirmed revisits before death:

```text
CONSUMED:HUNT revs=N
```

## Why this matters

A revisited live node is not the same as a virgin node. It is still live, but the
market has already interacted with its territory. This memory lets us later test
whether second/third revisits behave differently from first visits.

## Version

`M0001_LiveVisualLab.mq5` version: `1.41`.
