# Phase 18 — Minimal Readability / Qualified Hooks

## Problem

`MINIMAL_ALL_HOOKS` correctly removed the heavy P03/P04/P05/P06 overlays, but the chart was still visually busy because it rendered every raw candidate, including many `X1` structures. An `X1` structure is useful for raw debugging, but it is usually not a readable Hook.

The arc height was also too large on high-range moves, and arrow-style X markers still added unnecessary visual weight.

## Fix

Phase 18 adds readability controls to Phase 02:

```text
InpHookPhase02MinXCountToDraw
InpHookPhase02ArcMinXCountToDraw
InpHookPhase02CycleArcMaxHeightPoints
InpHookPhase02NodeNumberOffsetPoints
InpHookPhase02UseMinimalNodeMarkers
InpHookPhase02MinimalNodeMarkerArrowCode
```

## Minimal profile defaults

`FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS` now forces:

```text
min_x_count_to_draw = 2
arc_min_x_count_to_draw = 2
cycle_arc_height_ratio = 0.08
cycle_arc_max_height_points = 500
node_number_offset_points = 22
use_minimal_node_markers = true
minimal_node_marker_arrow_code = 159
```

So the view shows all **qualified** Hook sequences, not every one-node candidate.

## Meaning

- `X1` candidates are hidden by default.
- `X2+` Hook structures remain visible.
- Arcs are capped so they do not dominate the chart.
- Nodes use small neutral dot markers rather than directional arrow glyphs.
- Node numbers are offset slightly from the node price so they are readable.

## To show every raw candidate again

Set:

```text
InpHookPhase02MinXCountToDraw = 1
InpHookPhase02ArcMinXCountToDraw = 1
InpHookPhase02UseMinimalNodeMarkers = false
```
