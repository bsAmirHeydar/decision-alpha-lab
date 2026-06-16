# M0001 Live Visual Lab — Debug Packages

The live MQL expert is now package-based. It is designed for validating the RTV logic event by event instead of drawing every object at once.

Main expert:

```text
mql5/Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

## Preset selector

Use this input:

```text
InpViewPreset
```

Values:

```text
0  = Custom manual toggles
1  = Package 1  - Structural Node Audit
2  = Package 2  - Territory Construction Audit
3  = Package 3  - Event Entry Exit Audit
4  = Package 4  - Baseline vs Inside Sample Audit
5  = Package 5  - RTV Formula Audit
6  = Package 6  - Hunt Validation Audit
7  = Package 7  - Live Open Event Audit
8  = Package 8  - Candle Classification Audit
9  = Package 9  - State Machine Audit
10 = Package 10 - Focused Event Inspector
11 = Package 11 - Multi Event Overview
12 = Package 12 - Full Research Lab
```

## Focus selector

Use this input:

```text
InpFocusMode
```

Values:

```text
0 = latest event / none
1 = selected node/revisit
2 = latest closed event
3 = latest open event
4 = latest hunted event
5 = strongest RTV event
```

To inspect one exact event:

```text
InpViewPreset = 10
InpFocusMode = 1
InpSelectedNodeId = <node id>
InpSelectedRevisitId = <revisit id or -1>
```

## Package 1 — Structural Node Audit

Purpose: verify L-rule node detection and confirmation delay.

Shows:

```text
nodes
node labels
node price line
active_from line
confirmation window
```

Question answered:

```text
Did the node become usable only after node_index + L?
```

## Package 2 — Territory Construction Audit

Purpose: verify territory construction from node price and expansion extreme.

Shows:

```text
selected event/node
node price line
expansion extreme
territory upper/lower
territory box
zone ratio label
```

Question answered:

```text
Was territory built from the correct extreme and node_price?
```

## Package 3 — Event Entry Exit Audit

Purpose: verify start and end of the event.

Shows:

```text
event window
ENTRY marker
EXIT marker
outside_count labels
```

Question answered:

```text
Did the event start on the first wick touch and close after exit_gap outside candles?
```

## Package 4 — Baseline vs Inside Sample Audit

Purpose: verify the actual candles used in RTV.

Shows:

```text
before baseline candles = violet outline
inside candles = cyan outline
outside-active candles = orange outline
legend
```

Question answered:

```text
Are mean_before and mean_inside built from the correct candles?
```

## Package 5 — RTV Formula Audit

Purpose: verify the RTV number.

Shows:

```text
RTV label
formula card
mean_inside
mean_before
median_inside
median_before
counts
```

Question answered:

```text
Is RTV = mean_inside / mean_before correct?
```

## Package 6 — Hunt Validation Audit

Purpose: verify hunt detection.

Shows:

```text
node price line
hunt marker
hunt label
entry/exit context
```

Question answered:

```text
Was the first breach candle marked correctly?
```

## Package 7 — Live Open Event Audit

Purpose: inspect the currently open event.

Shows:

```text
open event window
live RTV
live counts
inside/before/outside state
```

Question answered:

```text
What is the event doing right now in live mode?
```

## Package 8 — Candle Classification Audit

Purpose: inspect candle-by-candle classification.

Shows:

```text
classification panel:
idx | range | log | B/I/O/HUNT flags
```

Flags:

```text
B = before baseline sample
I = inside sample
O = outside-active candle
HUNT = first hunt breach
```

Question answered:

```text
How did the engine classify each candle?
```

## Package 9 — State Machine Audit

Purpose: inspect state transitions.

Shows:

```text
NODE
EVENT_ENTERED
HUNTED
EXITED / OPEN
state timeline
transition markers
```

Question answered:

```text
Did the event state machine advance in the right order?
```

## Package 10 — Focused Event Inspector

Purpose: the main validation mode.

Shows:

```text
one selected/focused event only
territory
entry/exit
before/inside/outside samples
RTV formula
hunt marker
candle classification table
state timeline
inspector card
```

Recommended first serious debug mode:

```text
InpViewPreset = 10
InpFocusMode = 2
```

## Package 11 — Multi Event Overview

Purpose: broad overview without full clutter.

Shows:

```text
nodes
event windows
RTV labels
hunt markers
summary panel
```

Recommended when browsing market behavior.

## Package 12 — Full Research Lab

Purpose: everything at once.

Use it sparingly. It can still become visually dense.

## Recommended validation order

```text
1 -> Structural Node Audit
2 -> Territory Construction Audit
3 -> Event Entry Exit Audit
4 -> Baseline vs Inside Sample Audit
5 -> RTV Formula Audit
6 -> Hunt Validation Audit
10 -> Focused Event Inspector
```

## Performance tips

If MT5 becomes slow:

```text
InpLookbackBars = 500
InpMaxNodesToDraw = 80
InpMaxEventsToDraw = 30
InpViewPreset = 10
```

Package 10 is intentionally much cleaner than Package 12.
