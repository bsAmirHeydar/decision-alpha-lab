# Visual Replay Protocol

## Purpose

The Visual Replay Protocol defines how the UI replays market candles and overlays research artifacts on top of them.

The goal is to make every test visually inspectable as if it were running live.

---

## Central Concept

The replay view is controlled by one object:

```text
ReplaySession
```

A replay session contains:

```text
session_id
source
symbol
timeframe
start_time
end_time
current_time
current_index
speed
status
available_layers
active_layers
selection
```

---

## Replay Status

Valid replay states:

```text
idle
loading
ready
playing
paused
completed
error
```

---

## Timeline Rules

1. The chart must advance by candle index, not wall-clock time.
2. The current replay candle is the latest candle visible to the simulated system.
3. No visual object may appear before its `visible_from_index`.
4. L-rule nodes must become visible only after confirmation.
5. Metric events must become visible only when their event lifecycle reaches the current replay index.
6. Historical completed events may remain visible when the cursor moves forward.
7. Moving the cursor backward must restore the visual state that would have been known at that point.

---

## Core Replay Controls

The first UI implementation must include:

```text
Play
Pause
Step forward one candle
Step backward one candle
Jump to start
Jump to end
Speed selector
Manual candle index scrubber
```

Speed presets:

```text
1x
2x
5x
10x
25x
50x
100x
```

---

## Chart Layout

```text
┌─────────────────────────────────────────────────────────────┐
│ Header: symbol, timeframe, source, run, parameters           │
├─────────────────────────────────────────────────────────────┤
│ Toolbar: play/pause, speed, layers, filters                  │
├──────────────┬────────────────────────────────┬─────────────┤
│ Research     │ Main chart                     │ Inspector   │
│ tree         │ Candles + visual overlays      │ Details     │
│              │                                │             │
├──────────────┴────────────────────────────────┴─────────────┤
│ Bottom panel: dynamic tables, event rows, selected data      │
└─────────────────────────────────────────────────────────────┘
```

---

## Visual Layers

Every overlay must belong to a named layer.

Core layers:

```text
candles
structural_nodes
node_territories
metric_events
hunts
revisits
baseline_windows
rtv_values
annotations
```

Layer controls must support:

```text
show / hide
opacity
z-index order
filter by node type
filter by event status
filter by RTV range
```

---

## Selection Model

The UI has one global selection state:

```text
SelectionState
```

A selection may point to:

```text
candle
node
event
zone
hypothesis
experiment
metric_run
validation_run
signal
```

Selection must update:

- chart highlight
- bottom table selected row
- right inspector
- URL state if routing is enabled

---

## Hover Model

Hover is temporary and must not replace selection.

Hover may show:

- candle OHLC tooltip
- node tooltip
- event tooltip
- RTV quick summary
- territory bounds

---

## Candle Replay Semantics

At replay index `i`, the UI may show:

- candles with index `<= i`
- nodes with `visible_from_index <= i`
- active event state whose `entry_index <= i`
- completed event state whose `exit_index <= i`

The UI must not show:

- future candles
- future node confirmation
- future event termination
- final metric result before event completion, unless explicitly marked as preview/incomplete

---

## M0001 Replay Behavior

For M0001, the UI should support these visual elements:

```text
confirmed L-rule node marker
territory zone rectangle
active revisit window
exit gap countdown
hunt marker
consumed marker
RTV label after event completion
baseline sample window
inside sample window
```

M0001-specific overlays must still use the generic visualization API.

---

## Bottom Dynamic Table

The bottom table must change based on active context.

Examples:

```text
Selected metric run     → event table
Selected node           → node revisit table
Selected event          → event candle sample table
Selected experiment     → experiment result table
Selected validation     → robustness table
```

Table row selection must move the chart cursor to the related object.

---

## Inspector Panel

The inspector must show:

```text
object type
object id
source reference
research lineage
parameters
lifecycle state
numeric fields
related objects
links to files/reports
```

For example, selecting an M0001 event should show:

```text
node_id
node_type
node_time
node_price
revisit_id
entry_time
exit_time
event_length
territory_lower
territory_upper
expansion_extreme
mean_inside
mean_before
median_inside
median_before
RTV
hunted
source metric run
source hypothesis
source experiment
```

---

## Reproducibility Rule

A replay session must be restorable from:

```text
source
symbol
timeframe
metric_id
parameters
cache snapshot or run id
```

No visual state should depend on hidden local UI assumptions.
