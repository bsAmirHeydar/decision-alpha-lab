# Flag Counting Level 19 — Phase 10 Panel Line Debug Contract

## Purpose

Phase 10 makes the State Gate panel auditable line-by-line.

The problem solved by this phase is simple:

> Whatever the panel is supposed to show must also exist in a CSV row.

This is important because chart objects can be clipped, hidden, overlapped, collapsed, or affected by old MetaTrader input sets. The CSV contract lets the operator debug the dashboard without guessing.

## What Phase 10 adds

Phase 10 adds:

```text
InpStateGateExportPanelLinesCsv = true
```

and writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_panel_lines.csv
```

This file is a logical mirror of the expanded panel model.

It does not replace:

```text
latest_state_gate_panel.csv
latest_state_gate_diagnostics.csv
latest_state_gate_summary.csv
latest_state_gate_rally.csv
latest_state_gate_hooks.csv
latest_state_gate_contract.csv
```

It complements them by listing every dashboard line as an auditable row.

## CSV schema

`latest_state_gate_panel_lines.csv` contains:

```text
symbol
update_serial
line_index
slot
timeframe
section
line_type
preview_index
source_kind
source_id
effective_corner
panel_x
panel_y
text
closed_bar_time
state_key
contract_status
entry_bridge_status
```

## Line sections

The line contract exports global and per-timeframe lines:

```text
GLOBAL / HEADER
GLOBAL / DIAGNOSTICS
TF / SLOT_HEADER
TRACKER / TRACKER
COUNTS / ROW_COUNTS
CONTRACT / STATE_KEY
RALLY / SECTION_HEADER
RALLY / PREVIEW_ROW
RALLY / MORE_ROWS
HOOK / SECTION_HEADER
HOOK / PREVIEW_ROW
HOOK / MORE_ROWS
```

## Important boundary

Phase 10 is still **context-only**.

It does not add:

```text
buy
sell
entry_allowed
entry_direction
entry_price
stop
target
```

The `entry_bridge_status` field remains decision-neutral.

## Locked logic

Phase 10 does not modify:

- Node Engine
- Hook / ND Engine
- Flag Body
- Internal Count
- F1 Lifecycle
- F2 Lifecycle
- F3 Lifecycle
- Ownership / Canonicalization
- Renderer
- Validation
- Release
- License

Only Level 19 State Gate export/config surfaces are extended.

## How to use

After compile and run, open:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_panel_lines.csv
```

If the panel is not visible on the chart, this file shows what the panel attempted to display and where the effective corner/coordinates are.

The practical debug flow is:

```text
1. Check latest_state_gate_diagnostics.csv for corner and placement.
2. Check latest_state_gate_panel_lines.csv for every intended panel line.
3. Check latest_state_gate_rally.csv and latest_state_gate_hooks.csv for full row detail.
4. If panel text is clipped, increase InpStateGatePanelWidth.
5. If panel is off-screen, confirm ForceLeftUpper is true and X/Y are small.
```

## Status

Phase 10 completes the State Gate debug/export contract needed before entry-bridge fields.

The next natural phase is:

```text
Phase 11 — Entry Bridge Readiness Fields
```

Still without actual trade signals.
