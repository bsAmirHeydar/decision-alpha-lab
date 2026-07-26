# Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map

## Purpose

Phase 13 adds a decision-neutral Multi-Timeframe Alignment Map above the Extreme Candidate Map.

The State Gate now compares lower-slot context against higher-slot context.

Default slot order is interpreted as:

```text
slot 0 = lower timeframe context
slot 1 = middle timeframe context
slot 2 = higher timeframe context
```

With the default inputs, this means:

```text
M1  -> M10
M1  -> H1
M10 -> H1
```

## What Phase 13 does

Phase 13 reads the already-built Phase 12 Extreme Candidate Map and builds pair rows between configured timeframes.

It compares:

```text
child timeframe
parent timeframe
child extreme source
parent extreme source
child direction
parent direction
child side
parent side
child node/price context
parent node/price context
```

It then labels the relationship with decision-neutral alignment fields.

## New CSV

Phase 13 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_mtf_alignment.csv
```

This is the primary Phase 13 output.

## New per-timeframe fields

Each State Gate timeframe state now has:

```text
mtf_alignment_row_count
mtf_alignment_status
mtf_alignment_key
mtf_parent_timeframe
mtf_parent_extreme_key
mtf_parent_direction
mtf_parent_side
mtf_direction_relation
mtf_side_relation
mtf_context_role
mtf_alignment_notes
```

## Alignment labels

Direction relationship:

```text
MTF_DIRECTION_ALIGNED
MTF_DIRECTION_DIVERGENT
MTF_DIRECTION_UNKNOWN
```

Side relationship:

```text
MTF_SAME_EXTREME_SIDE
MTF_OPPOSITE_EXTREME_SIDE
MTF_SIDE_PENDING
MTF_SIDE_UNKNOWN
```

Context role:

```text
LTF_EXTREME_WITH_HTF_CONTEXT_ALIGNED
LTF_DIRECTION_ALIGNED_HTF_OPPOSITE_SIDE_CONTEXT
LTF_HTF_DIRECTION_DIVERGENCE_CONTEXT
MTF_CONTEXT_PENDING_RALLY_SIDE
MTF_CONTEXT_INCOMPLETE
HTF_TOP_LEVEL_CONTEXT
```

Readiness examples:

```text
MTF_ALIGNMENT_READY_CONTEXT_ONLY_NO_DECISION
MTF_ALIGNMENT_BLOCKED_CHILD_NO_CLOSED_BAR
MTF_ALIGNMENT_BLOCKED_PARENT_NO_CLOSED_BAR
MTF_ALIGNMENT_BLOCKED_CHILD_NO_EXTREME
MTF_ALIGNMENT_BLOCKED_PARENT_NO_EXTREME
MTF_TOP_CONTEXT_READY_NO_PARENT
MTF_TOP_CONTEXT_NO_EXTREME
```

All labels remain context-only and decision-neutral.

## What Phase 13 does not do

Phase 13 does not produce:

```text
buy
sell
entry_allowed
entry_price
stop_loss
take_profit
order_type
```

It only explains whether lower-timeframe candidate extremes make sense relative to higher-timeframe context.

## Updated exports

Phase 13 extends:

```text
latest_state_gate_summary.csv
latest_state_gate_panel.csv
latest_state_gate_panel_lines.csv
latest_state_gate_contract.csv
latest_state_gate_entry_bridge.csv
latest_state_gate_manifest.csv
```

and adds:

```text
latest_state_gate_mtf_alignment.csv
```

## New input

```text
InpStateGateExportMtfAlignmentCsv = true
```

## Locked boundaries

Phase 13 does not modify:

```text
Node Engine
Hook / ND Engine
Flag Body
Internal Count
F1 Lifecycle
F2 Lifecycle
F3 Lifecycle
Ownership / Canonicalization
Renderer
Validation
Release
License
```

It only reads projected Level 19 State Gate context.

## Next natural phase

The next phase is:

```text
Phase 14 — Entry Geometry Readiness
```

That phase should still avoid orders, but can start preparing candidate entry price, invalidation price, destination price, and potential R fields from the mapped X context.
