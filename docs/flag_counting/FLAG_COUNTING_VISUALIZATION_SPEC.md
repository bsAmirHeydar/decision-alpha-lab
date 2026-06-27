# Flag Counting Visualization Specification

Version: v1  
Scope: visual rendering contract for the FlagCountingVNext experiment.

This document defines how F-counting structures must be displayed on a MetaTrader chart. The goal is to keep the chart readable while preserving the fractal, multi-scale, multi-sequence nature of the model.

## 1. Rendering Principles

The renderer must not behave like a raw candidate dump. It must show accepted or diagnostic flag-counting structures in a way that preserves hierarchy and avoids visual confusion.

Core principles:

1. Higher scale has higher visual priority.
2. Larger scale structures must look visually stronger.
3. F-level labels must not overlap; they must be vertically stacked.
4. The chart must stay body-only by default.
5. Internal `1` and `2` are labels only, not connected with extra lines.
6. Direction and status must both be visible.
7. Debug overlays must be optional and off by default.

## 2. Body-only Rendering Contract

Each F body is rendered as:

- `Origin -> Leg1`: one straight trend line.
- `Leg1 -> Waist -> Leg2`: one smooth curve, made of several short trend segments.
- `F1`, `F2`, or `F3`: small level label near Leg2.
- `1` and `2`: small numeric labels only, placed on their own nodes.

The renderer must not draw post-Leg2 lines by default:

- no `Leg2 -> internal 1` line,
- no `internal 1 -> internal 2` line,
- no `internal 2 -> confirm` line.

Those relationships belong to calculation and audit. They may be shown only in an explicit debug mode.

## 3. Scale Priority

When multiple structures overlap, the renderer must sort them by scale before drawing.

Recommended order:

1. Draw smaller scale first.
2. Draw larger scale later, so larger scale appears on top.
3. Label placement should reserve more spacing for larger scales.

This gives higher scale structures visual dominance without deleting lower scale structures.

## 4. Scale-aware Line Width

Line width must be derived from scale rank, not from arbitrary F-level.

Recommended mapping:

- Smallest active scale: width 1
- Middle scale: width 2
- Large scale: width 3
- Very large scale: width 4

The exact mapping can be parameterized, but larger scale should never be visually weaker than smaller scale.

## 5. Scale-aware Font Size

F-level labels and internal labels should be tiny by default, but scale-aware.

Recommended mapping:

- Small scale F label: 6 to 7
- Middle scale F label: 8 to 9
- Large scale F label: 10 to 11
- Internal `1/2`: same or slightly smaller than the F-level label for that scale

The purpose is to make the visual hierarchy readable without turning the chart into text noise.

## 6. Label Stacking

F-level labels must not be placed directly on top of each other.

The renderer should compute a label lane for each visible event near its Leg2 or current body endpoint.

Recommended algorithm:

1. Start from the natural label anchor near Leg2.
2. Look for existing labels in the same time/price neighborhood.
3. If overlap is detected, move the new label one lane up for bullish structures or one lane down for bearish structures.
4. Repeat until the label does not overlap an already reserved lane.
5. Larger scale labels reserve wider lanes.

This creates vertical stacking instead of unreadable label collisions.

## 7. Direction and Status Colors

The visualization must communicate two independent concepts:

- direction: bullish or bearish,
- state: live/pending or confirmed.

This requires four colors.

Recommended default:

- Bullish live: cyan or bright blue
- Bullish confirmed: lime or green
- Bearish live: orange
- Bearish confirmed: red or tomato

F-level must be shown through the label text (`F1`, `F2`, `F3`), not through the main color. Color should primarily mean direction and state.

## 8. F3 Terminal Rendering

F3 is special. Once F3 completes its two-leg body, the sequence is considered structurally complete. The post-F3 movement is terminal behavior and may reverse or continue in a special way.

Rendering rule:

- F3 body should still use body-only rendering.
- Post-F3 movement should not be connected by default.
- If shown, post-F3 terminal behavior must use a distinct optional debug color/style.

## 9. Multi-scale Display Modes

The renderer should support these display modes:

1. Selected scale only.
2. All scales.
3. Dominant sequences only.
4. Debug all accepted sequences.

Default for research can be all scales, but with max draw limits and scale-aware label/line weights.

## 10. Conflict Resolver Display

When multiple sequences are almost identical, the renderer should avoid drawing duplicates.

Two structures may be considered visual duplicates when:

- they have the same direction,
- same F-level,
- same or near-identical Origin, Leg1, Waist, and Leg2 time range,
- same scale or nearly adjacent scale,
- similar price body.

If duplicates exist, prefer:

1. higher scale,
2. confirmed over live,
3. higher F-level,
4. cleaner geometry,
5. larger body if the above are equal.

## 11. Debug Visibility

The default chart must be clean. Debug mode can optionally show:

- rejected candidates,
- invalidation lines,
- confirmation points,
- parent-child links,
- sequence IDs,
- scale IDs,
- ND/Hook segments.

All debug overlays must be off by default.

## 12. Suggested Renderer Inputs

Recommended inputs:

- `InpDrawF1`
- `InpDrawF2`
- `InpDrawF3`
- `InpDrawOnlyConfirmed`
- `InpDrawBullish`
- `InpDrawBearish`
- `InpDrawAllScales`
- `InpSelectedScaleL`
- `InpMaxEventsToDraw`
- `InpUseScaleAwareWidth`
- `InpUseScaleAwareFont`
- `InpStackLabels`
- `InpShowInternal12Labels`
- `InpShowDebugLinks`
- `InpShowND`

## 13. Acceptance Criteria

A visualization pass is acceptable only if:

1. The chart never shows all raw candidates as spaghetti.
2. Higher scale structures are visually stronger than lower scale structures.
3. F labels do not overlap heavily.
4. Internal `1` and `2` are readable but not dominant.
5. Bullish and bearish structures are distinguishable by color.
6. Live and confirmed structures are distinguishable by color or style.
7. F1/F2/F3 labels show the F-level without requiring different F-level colors.
8. The body is clean: straight first leg and curved Leg1-Waist-Leg2 body.
9. Debug lines are hidden unless explicitly requested.
10. The renderer can be used to inspect multi-scale parallel sequences without destroying chart readability.

## 14. Implementation Note

This document is a visualization contract. It does not change the F-counting grammar. The renderer must consume accepted events from the detector and apply visual prioritization, stacking, and scale-aware styling.
