# Flag Counting Level 19 — Phase 15 Entry Idea Layer

## Purpose

Phase 15 adds the first decision-neutral Entry Idea Layer above Entry Geometry Readiness.

This phase still does **not** create executable trade signals.

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

It only wraps the available geometry/context into idea-only records.

## New CSV

Phase 15 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_entry_ideas.csv
```

This is the primary Phase 15 output.

## New input

```text
InpStateGateExportEntryIdeasCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
entry_idea_row_count
entry_idea_status
entry_idea_readiness
entry_idea_key
primary_entry_idea_family
primary_entry_idea_type
primary_entry_idea_direction
primary_entry_idea_source
primary_entry_idea_role
primary_entry_idea_geometry_status
primary_entry_idea_mtf_context
entry_idea_notes
```

## Idea families

The idea layer classifies context into idea families:

```text
MTF_ALIGNED_HOOK_EXTREME_IDEA_ONLY
HOOK_EXTREME_REVERSAL_IDEA_ONLY
RALLY_CONTEXT_EXTREME_IDEA_ONLY
GEOMETRY_CONTEXT_IDEA_ONLY
ENTRY_IDEA_PENDING_CONTEXT_ONLY
ENTRY_IDEA_BLOCKED_NO_ENTRY_GEOMETRY
ENTRY_IDEA_BLOCKED_NO_CLOSED_BAR
```

## Idea types

Examples:

```text
SELECTED_EXTREME_REVERSION_CONTEXT_IDEA_ONLY
RALLY_STAGE_CONTEXT_IDEA_ONLY
GEOMETRY_CONTEXT_IDEA_ONLY
WAIT_FOR_ENTRY_GEOMETRY_IDEA_ONLY
```

## Readiness labels

Examples:

```text
ENTRY_IDEA_READY_FOR_DRY_RUN_NO_SIGNAL_NO_ORDER
ENTRY_IDEA_PARTIAL_DESTINATION_PENDING_NO_SIGNAL_NO_ORDER
ENTRY_IDEA_BLOCKED_NO_ENTRY_ANCHOR
ENTRY_IDEA_BLOCKED_NO_CLOSED_BAR
```

## What the row contains

Each entry idea row exports:

```text
timeframe
idea_family
idea_type
idea_direction
idea_source
idea_role
geometry_status
mtf_context_role
extreme_side
entry_price
invalidation_anchor_price
destination_anchor_price
destination_distance
risk_status
potential_R_status
idea_key
label
```

These are still anchors and ideas, not orders.

## Design boundary

Phase 15 converts:

```text
State Gate anatomy
Extreme Candidate Map
MTF Alignment Map
Entry Geometry Readiness
```

into:

```text
Entry Idea Layer
```

But the idea layer remains explicitly non-executable.

The next phase can use these idea rows to simulate hypothetical dry-run decisions, but Phase 15 itself does not approve, send, or size trades.

## Locked boundaries

Phase 15 does not modify:

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

It only reads Level 19 State Gate context and exports idea-only records.

## Next natural phase

The next phase is:

```text
Phase 16 — Entry Decision Layer
```

However, to keep the research clean, Phase 16 should still be dry-run first:

```text
entry_decision_status
entry_decision_direction
entry_decision_type
entry_decision_price
entry_decision_invalidaton
entry_decision_destination
entry_decision_allowed = false by default
```

No real order should be sent until a later execution adapter phase.
