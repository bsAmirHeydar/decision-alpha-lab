# Flag Counting Phoenix — Level 19 Phase 5 Panel Polish and Debug Usability

## Purpose

Phase 5 keeps the Level 19 State Gate as a read-only anatomy layer and improves how the state map can be used live.

The goal is not to add entry logic.
The goal is to make the State Gate easier to read, debug, and use as the future bridge between anatomy and entry design.

Phase 5 improves:

```text
right-upper dashboard anchoring
panel readability
Rally row preview control
Hook row preview control
compact labels
row-count visibility
closed-bar visibility
no-data / dirty-state coloring
panel-debug CSV export
manifest fields for dashboard configuration
```

The locked anatomy engines remain untouched.

## Hard boundary

Phase 5 does not change any of these layers:

```text
Node Engine
Node Canonicalizer
Hook / ND Engine
Flag Body Engine
Internal Count Engine
F1 Lifecycle Engine
F2 Lifecycle Engine
F3 Lifecycle Engine
Ownership Engine
Canonicalization
Renderer
Validation
Release profiles
License gate
```

Phase 5 only changes the Level 19 State Gate presentation, export metadata, and dashboard usability.

## Conceptual role

The State Gate is not a dashboard-only feature.
It is the live state gate that stores the current multi-timeframe anatomy in a stable format.

The dashboard is the visible face of that gate.

```text
State Gate = live anatomy state store
Dashboard  = chart UI for seeing and debugging that state
CSV export = audit trail for validating what the dashboard saw
```

This matters because the project will later connect anatomy to entry. Phase 5 makes the anatomy state readable enough that future entry design can be discussed without guessing what the market state was.

## Closed-bar rule remains unchanged

Phase 5 continues the Phase 2 rule:

```text
Only the last closed candle, shift=1, is canonical for State Gate state.
```

The live forming candle is not used as canonical State Gate state.

## Dashboard position

The dashboard is designed for the upper-right chart corner.

Default inputs:

```text
InpStateGatePanelCorner = CORNER_RIGHT_UPPER
InpStateGatePanelX      = 16
InpStateGatePanelY      = 24
```

Phase 5 adds:

```text
InpStateGatePanelForceRightUpper = true
```

When enabled, all Level 19 chart objects are forced to `CORNER_RIGHT_UPPER` even if the older corner input is changed. This makes the dashboard position stable and matches the intended layout.

## New Phase 5 inputs

```text
InpStateGatePanelRallyPreviewRows = 2
InpStateGatePanelHookPreviewRows  = 2
InpStateGatePanelForceRightUpper  = true
InpStateGatePanelCompactMode      = true
InpStateGatePanelShowClosedBar    = true
InpStateGatePanelShowRowCounts    = true
```

These inputs affect only the dashboard presentation.
They do not change the stored State Gate snapshot and do not change the underlying Rally or Hook projections.

## Preview rows versus stored rows

Phase 5 separates stored state from visible preview.

For example:

```text
InpStateGateMaxRallyRowsPerTf = 6
InpStateGateMaxHookRowsPerTf  = 10
```

control how many rows are stored per timeframe.

But:

```text
InpStateGatePanelRallyPreviewRows = 2
InpStateGatePanelHookPreviewRows  = 2
```

control how many of those rows are shown on the chart panel.

If more rows exist than the panel preview allows, the panel displays a continuation hint:

```text
R+ | 4 more Rally rows in CSV
H+ | 8 more Hook rows in CSV
```

The full rows remain available in:

```text
latest_state_gate_rally.csv
latest_state_gate_hooks.csv
```

## Compact labels

When enabled:

```text
InpStateGatePanelCompactMode = true
```

Rally and Hook rows are shortened for live readability.

A Rally row becomes a compact state line such as:

```text
R1 | M1 F2 | bullish | F2_ESTABLISHED|bullish|confirmed | L8 | E#104
```

A Hook row becomes a compact state line such as:

```text
H1 | M10 Hook | L13 | POSITIVE_HOOK_REVERSAL_UP | N3 | H#188 | L#191 | Hk#44
```

When compact mode is disabled, the panel uses the longer internal row labels.

## Dirty and no-data colors

Phase 5 makes timeframe status easier to see:

```text
DIRTY / new closed bar       = light blue
UNCHANGED / already processed = light steel blue
NO_DATA / unavailable         = tomato
projected Rally rows          = silver
projected Hook rows           = light green
unknown/no-row states          = tomato
```

These colors are only dashboard presentation. They do not change State Gate logic.

## Row-count line

When enabled:

```text
InpStateGatePanelShowRowCounts = true
```

Each timeframe block includes a row-count line:

```text
rows | rally=6 hook=10 | status=CLOSED_BAR_CHANGED
```

This is useful when debugging whether the State Gate is storing more state than the panel preview currently displays.

## Closed-bar line

When enabled:

```text
InpStateGatePanelShowClosedBar = true
```

Each timeframe header includes:

```text
closed=<closed-bar-time>
close=<closed-bar-close>
updates=<update-count>
```

This confirms that the panel is showing closed-bar state, not live candle noise.

## Minimize / restore

The minimize button remains isolated to the Level 19 object prefix.

```text
- = minimize
+ = restore
```

When minimized, the panel preserves the runtime state and only hides the expanded rows. The State Gate continues to update and export if enabled.

## Panel object ownership

All dashboard objects use the configured Level 19 prefix:

```text
FP_L19_STATE_GATE_
```

Before each redraw, Phase 5 deletes only objects with that prefix. It never deletes Phoenix renderer objects, user chart drawings, or other project layers.

## New panel-debug CSV

Phase 5 adds:

```text
latest_state_gate_panel.csv
```

This file stores one row per configured timeframe with the exact dashboard-control state:

```text
symbol
slot
timeframe
dirty
closed_bar_time
closed_bar_close
rally_rows_total
hook_rows_total
rally_preview_limit
hook_preview_limit
latest_established_f_summary
probable_next_f_summary
hook_summary
tracker_status
reason
```

This is not a replacement for the full Rally and Hook CSVs. It is a compact debug file for verifying what the panel should be showing.

## Manifest additions

The State Gate manifest now records dashboard configuration:

```text
panel_force_right_upper
panel_corner_effective
panel_width
panel_font_size
panel_compact_mode
panel_show_closed_bar
panel_show_row_counts
panel_rally_preview_rows_per_tf
panel_hook_preview_rows_per_tf
projection_state = phase5_rally_hook_panel_polished
```

## Acceptance criteria

Phase 5 is accepted when:

```text
1. The dashboard appears in the upper-right chart corner by default.
2. `InpStateGatePanelForceRightUpper=true` forces the upper-right corner.
3. The panel shows closed-bar state for each configured timeframe.
4. Rally preview rows are controlled by `InpStateGatePanelRallyPreviewRows`.
5. Hook preview rows are controlled by `InpStateGatePanelHookPreviewRows`.
6. More-row hints appear when stored rows exceed preview rows.
7. The panel can minimize and restore without touching non-Level-19 objects.
8. `latest_state_gate_panel.csv` is exported when CSV export is enabled.
9. The manifest records the Phase 5 panel configuration.
10. Node, Hook/ND, F1, F2, F3, ownership, canonicalization, renderer, validation, release, and license logic remain unchanged.
```

## What Phase 5 is not

Phase 5 is not an entry engine.

It does not output:

```text
buy
sell
entry allowed
entry forbidden
stop
target
risk
reward
```

It only makes the multi-timeframe anatomy gate clear enough that a future entry layer can be designed on top of it.
