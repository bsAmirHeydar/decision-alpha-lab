# Flag Counting Level 19 — Phase 9 Visual Debug Contract

## Purpose

Phase 9 turns the State Gate panel and CSV exports into a stronger debug contract.

The previous phases built:

- closed-bar timeframe tracking
- Rally View projection
- Hook View projection
- panel usability
- State Contract storage
- left-upper panel forcing

Phase 9 does not add entry logic. It makes the existing State Gate easier to verify after compile and easier to debug on a live chart.

## Core principle

Level 19 remains a read-only projection layer.

It reads the locked anatomy outputs and exposes them as:

```text
dashboard
summary CSV
rally CSV
hook CSV
panel CSV
contract CSV
diagnostics CSV
manifest CSV
```

It must not mutate the anatomy engines.

## Locked engines

Phase 9 does not change:

```text
Node Engine
Hook / ND Engine
Flag Body Engine
Internal Count Engine
F1 Lifecycle Engine
F2 Lifecycle Engine
F3 Lifecycle Engine
Ownership / Canonicalization
Renderer
Validation
Release
License
```

## New inputs

```text
InpStateGatePanelShowDiagnostics = true
InpStateGateExportDiagnosticsCsv = true
```

These are diagnostic-only switches.

## Panel diagnostics line

When enabled, the dashboard shows a diagnostics line near the top:

```text
diag | CORNER_LEFT_UPPER_FORCED|x=16|y=24|w=560|font=8 | serial=... | available=... | no_data=...
```

This line exists for two reasons:

1. to make the panel body obviously visible on the chart
2. to prove which corner and placement policy the EA is actually using

## Effective corner priority

The effective panel corner is now documented and exported.

Priority:

```text
ForceLeftUpper
then ForceRightUpper
then PanelCorner
```

So if `InpStateGatePanelForceLeftUpper=true`, the panel must use the upper-left chart corner even if older saved input sets still contain right-corner values.

## Diagnostics CSV

Phase 9 adds:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_diagnostics.csv
```

The diagnostics CSV includes one global row and one row per configured timeframe.

It records:

```text
state_gate_version
effective_corner
force_left_upper
force_right_upper
panel_corner_input
panel_x
panel_y
panel_width
panel_font_size
panel_enabled
panel_show_diagnostics
closed_bar_available
dirty
tracker_status
rally_rows
hook_rows
state_key
reason
```

This file is the first place to check when the panel looks wrong.

## Manifest additions

The manifest now includes:

```text
panel_force_left_upper
panel_force_right_upper
panel_corner_input
panel_corner_effective
panel_x
panel_y
panel_show_diagnostics
export_diagnostics_csv
projection_state = phase9_visual_debug_contract
```

## Acceptance checklist

After applying Phase 9, verify:

1. MetaEditor compile finishes.
2. The dashboard body is visible, not only the buttons.
3. The panel is in the upper-left chart corner when `InpStateGatePanelForceLeftUpper=true`.
4. The top diagnostics line appears when `InpStateGatePanelShowDiagnostics=true`.
5. `latest_state_gate_diagnostics.csv` is written when `InpStateGateExportDiagnosticsCsv=true`.
6. Rally / Hook / State Contract rows are still read-only projections.

## If the panel is still invisible

Check the EA inputs manually:

```text
InpStateGatePanelForceLeftUpper  = true
InpStateGatePanelForceRightUpper = false
InpStateGatePanelCorner          = CORNER_LEFT_UPPER
InpStateGatePanelX               = 16
InpStateGatePanelY               = 24
InpStateGatePanelWidth           = 560
InpStateGatePanelShowDiagnostics = true
```

If MT5 saved old values, load defaults or change these values manually.

## Status

Phase 9 is still context-only.

It does not produce:

```text
buy
sell
entry_allowed
entry_price
stop
target
```

The entry bridge remains for later phases.
