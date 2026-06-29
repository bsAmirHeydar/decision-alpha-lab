# Flag Counting Level 19 — Phase 17 Paper Execution / Dry Run Ledger

## Purpose

Phase 17 adds a paper execution ledger above the dry-run Entry Decision Layer.

This phase still does **not** send real orders.

The hard safety contract is:

```text
real execution = disabled
paper ledger only
decision_allowed remains false
```

## New CSV

Phase 17 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_ledger.csv
```

This file records the dry-run decision snapshot as a paper ledger row.

## New input

```text
InpStateGateExportPaperLedgerCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
paper_ledger_row_count
paper_ledger_status
paper_ledger_record_status
paper_ledger_key
paper_ledger_event_id
paper_ledger_mode
paper_ledger_direction
paper_ledger_type
paper_ledger_entry_price
paper_ledger_invalidation_price
paper_ledger_destination_price
paper_ledger_lifecycle_status
paper_ledger_execution_status
paper_ledger_source_decision_key
paper_ledger_notes
```

## Ledger record status

Examples:

```text
PAPER_LEDGER_RECORDED_DRY_RUN_ONLY
PAPER_LEDGER_BLOCKED_NO_CLOSED_BAR
PAPER_LEDGER_BLOCKED_NO_DECISION
PAPER_LEDGER_BLOCKED_NO_DECISION_PRICE
```

## Ledger lifecycle status

Examples:

```text
PAPER_LIFECYCLE_HYPOTHETICAL_OPEN_WITH_DESTINATION_ANCHOR
PAPER_LIFECYCLE_HYPOTHETICAL_OPEN_DESTINATION_PENDING
PAPER_LIFECYCLE_NOT_OPEN_NO_ENTRY_PRICE
```

## Execution safety

Every Phase 17 ledger row keeps:

```text
decision_allowed = false
execution_status = REAL_EXECUTION_DISABLED_PHASE17_PAPER_ONLY
ledger_mode      = PAPER_DRY_RUN_ONLY
```

No order is opened, modified, deleted, or sent.

## What the ledger row contains

Each paper ledger row exports:

```text
recorded_at
closed_bar_time
record_status
ledger_mode
lifecycle_status
decision_status
decision_readiness
decision_direction
decision_type
decision_allowed
entry_price
invalidation_price
destination_price
risk_status
potential_R_status
source_decision_key
source_idea_key
source_geometry_key
source_mtf_key
execution_status
block_reason
ledger_key
event_id
label
```

## Design boundary

Phase 17 converts:

```text
Entry Decision Dry Run
```

into:

```text
Paper Ledger Snapshot
```

but it does not create a persistent broker order, position, ticket, or live execution state.

## Locked boundaries

Phase 17 does not modify:

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

It only reads the Level 19 State Gate decision context and exports paper-only ledger records.

## Next natural phase

The next phase can be:

```text
Phase 18 — Paper Ledger Lifecycle Tracking
```

That phase should still be non-executable, but can evaluate whether a paper ledger row would have hit:

```text
hypothetical entry
hypothetical invalidation
hypothetical destination
hypothetical path state
```

using closed candles only.
