# Flag Counting Level 19 — Phase 14 Entry Geometry Readiness

## Purpose

Phase 14 prepares entry geometry fields from the existing State Gate context.

This phase is still **not** an entry system and still does **not** send orders.

It does not produce:

```text
buy
sell
entry_allowed
entry_direction
order_type
limit_order
market_order
stop_loss
take_profit
position_size
```

The purpose is only to answer:

```text
Do we have an entry anchor?
Do we have an invalidation anchor?
Do we have a destination anchor?
Can destination distance be measured?
Is potential R computable yet?
```

## New CSV

Phase 14 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_entry_geometry.csv
```

This file is the primary Phase 14 output.

## New per-timeframe fields

Each configured State Gate timeframe now stores:

```text
candidate_entry_price_status
candidate_entry_price
candidate_invalidation_price_status
candidate_invalidation_price
candidate_destination_price_status
candidate_destination_price
risk_distance_status
risk_distance
destination_distance_status
destination_distance
potential_R_status
potential_R
geometry_readiness
geometry_key
geometry_notes
```

## Geometry logic

### Entry anchor

If the Phase 12 Extreme Candidate Map produced a primary Hook-derived extreme with a price, Phase 14 sets:

```text
ENTRY_PRICE_ANCHOR_FROM_PRIMARY_EXTREME_NO_SIGNAL
```

The price is stored in:

```text
candidate_entry_price
```

This is not an executable entry. It is only a geometry anchor.

### Invalidation anchor

If an entry anchor exists, the invalidation anchor is set to the same primary extreme price:

```text
INVALIDATION_ANCHOR_FROM_PRIMARY_EXTREME_NEEDS_BUFFER_NO_STOP
```

This means:

```text
the structural invalidation area exists
but a real stop still needs a future buffer / stop model
```

So the phase does not create a stop-loss.

### Destination anchor

If the selected primary extreme comes from Hook context, Phase 14 tries to use the opposite Hook node:

```text
LOW_EXTREME  -> latest high node as destination anchor
HIGH_EXTREME -> latest low node as destination anchor
```

If found, status becomes:

```text
DESTINATION_ANCHOR_FROM_OPPOSITE_HOOK_NODE_NO_TARGET
```

Again, this is not a target order. It is only a destination anchor.

### Distance and R

Phase 14 can measure:

```text
destination_distance = abs(destination_anchor - entry_anchor)
```

But it does not compute executable R because real risk still requires a buffer/stop model.

Therefore:

```text
risk_distance_status = RISK_DISTANCE_PENDING_INVALIDATION_BUFFER_NO_POSITION
potential_R_status   = POTENTIAL_R_PENDING_RISK_BUFFER_NO_SIGNAL
potential_R          = 0
```

## Readiness labels

Examples:

```text
ENTRY_GEOMETRY_PARTIAL_READY_NO_SIGNAL
ENTRY_GEOMETRY_ENTRY_ANCHOR_READY_DESTINATION_PENDING_NO_SIGNAL
ENTRY_GEOMETRY_PENDING_PRICE_CONTEXT_NO_SIGNAL
ENTRY_GEOMETRY_BLOCKED_NO_EXTREME
ENTRY_GEOMETRY_BLOCKED_NO_CLOSED_BAR
```

## Updated exports

Phase 14 extends:

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
latest_state_gate_entry_geometry.csv
```

## New input

```text
InpStateGateExportEntryGeometryCsv = true
```

## Locked boundaries

Phase 14 does not modify:

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

It only reads Level 19 State Gate context and writes geometry-readiness fields.

## Next natural phase

The next phase is:

```text
Phase 15 — Entry Idea Layer
```

That phase should still avoid execution, but can label non-executable ideas such as:

```text
HOOK_EXTREME_REVERSAL_IDEA_NO_ORDER
MTF_ALIGNED_EXTREME_IDEA_NO_ORDER
RALLY_CONTEXT_PULLBACK_IDEA_NO_ORDER
```
