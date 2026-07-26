# Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run

## Purpose

Phase 16 adds the first Entry Decision Layer above the Entry Idea Layer.

This phase is still **non-executable**.

It does not send orders and it does not allow orders.

Phase 16 does not produce real execution fields such as:

```text
real_buy
real_sell
send_order
position_size
market_order
limit_order_submit
stop_loss_submit
take_profit_submit
```

The core safety invariant is:

```text
entry_decision_allowed = false
execution_status       = REAL_EXECUTION_DISABLED_PHASE16_DRY_RUN_ONLY
```

## New CSV

Phase 16 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_entry_decisions.csv
```

This is the primary Phase 16 output.

## New input

```text
InpStateGateExportEntryDecisionsCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
entry_decision_row_count
entry_decision_status
entry_decision_readiness
entry_decision_key
entry_decision_direction
entry_decision_type
entry_decision_mode
entry_decision_allowed
entry_decision_price_status
entry_decision_price
entry_decision_invalidation_status
entry_decision_invalidation_price
entry_decision_destination_status
entry_decision_destination_price
entry_decision_risk_status
entry_decision_potential_R_status
entry_decision_block_reason
entry_decision_execution_status
entry_decision_notes
```

## Decision direction

Phase 16 maps idea direction into a dry-run direction only:

```text
BULLISH -> BUY_DRY_RUN_ONLY
BEARISH -> SELL_DRY_RUN_ONLY
unknown -> NO_ENTRY_DECISION_DIRECTION
```

This is not an order direction. It is only a dry-run label.

## Decision type

Examples:

```text
LIMIT_AT_SELECTED_HOOK_EXTREME_DRY_RUN_ONLY
LIMIT_AT_RALLY_CONTEXT_EXTREME_DRY_RUN_ONLY
LIMIT_AT_GEOMETRY_ANCHOR_DRY_RUN_ONLY
WAIT_FOR_ENTRY_ANCHOR_DRY_RUN
```

These are decision labels only. They do not place limit orders.

## Readiness labels

Examples:

```text
ENTRY_DECISION_READY_DRY_RUN_NO_ORDER
ENTRY_DECISION_PARTIAL_DESTINATION_PENDING_DRY_RUN_ONLY
ENTRY_DECISION_BLOCKED_NO_ENTRY_PRICE
ENTRY_DECISION_BLOCKED_NO_ENTRY_IDEA
ENTRY_DECISION_BLOCKED_NO_CLOSED_BAR
```

## Execution safety

Every Phase 16 row keeps:

```text
decision_allowed = false
```

and exports:

```text
REAL_EXECUTION_DISABLED_PHASE16_DRY_RUN_ONLY
```

This guarantees Phase 16 remains research-only.

## What the row contains

Each entry decision row exports:

```text
timeframe
readiness
decision_status
decision_direction
decision_type
decision_mode
decision_allowed
decision_price
invalidation_price
destination_price
risk_status
potential_R_status
source_idea_key
source_geometry_key
source_mtf_key
block_reason
execution_status
decision_key
label
```

## Relationship to prior phases

Phase 16 consumes:

```text
Phase 11 — Entry Bridge Readiness
Phase 12 — Extreme Candidate Map
Phase 13 — Multi-Timeframe Alignment Map
Phase 14 — Entry Geometry Readiness
Phase 15 — Entry Idea Layer
```

and produces:

```text
Phase 16 — Entry Decision Dry Run
```

## Locked boundaries

Phase 16 does not modify:

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

It only reads Level 19 State Gate context and exports dry-run decision records.

## Next natural phase

The next phase is:

```text
Phase 17 — Paper Execution / Dry Run Ledger
```

That phase should record hypothetical fills and outcomes in a ledger, while still keeping real execution disabled.
