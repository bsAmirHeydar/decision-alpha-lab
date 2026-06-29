# Flag Counting Level 19 — Phase 18 Paper Ledger Lifecycle Tracking

## Purpose

Phase 18 adds paper lifecycle tracking above the Phase 17 Paper Ledger.

This phase still does **not** send real orders.

It evaluates the paper ledger against the latest closed candle close only and records whether the hypothetical paper anchors appear touched.

## Hard safety contract

```text
real execution = disabled
paper lifecycle only
no broker orders
no tickets
no position state
```

The lifecycle output is for research and inspection only.

## New CSV

Phase 18 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_lifecycle.csv
```

## New input

```text
InpStateGateExportPaperLifecycleCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
paper_lifecycle_row_count
paper_lifecycle_status
paper_lifecycle_key
paper_lifecycle_event_id
paper_lifecycle_path_state
paper_entry_touch_status
paper_invalidation_touch_status
paper_destination_touch_status
paper_lifecycle_outcome
paper_lifecycle_execution_status
paper_lifecycle_notes
```

## Evaluation method

Phase 18 uses the latest closed candle close only.

For a paper BUY direction:

```text
entry / invalidation touch: close <= anchor
destination touch:          close >= anchor
```

For a paper SELL direction:

```text
entry / invalidation touch: close >= anchor
destination touch:          close <= anchor
```

This is intentionally simple and conservative. It does not use intrabar high/low yet.

## Touch status examples

```text
PAPER_ENTRY_ANCHOR_TOUCHED_BY_CLOSED_CLOSE_ONLY
PAPER_ENTRY_ANCHOR_NOT_TOUCHED_BY_CLOSED_CLOSE_ONLY
PAPER_INVALIDATION_ANCHOR_TOUCHED_NO_STOP_NO_ORDER
PAPER_INVALIDATION_ANCHOR_NOT_TOUCHED
PAPER_DESTINATION_ANCHOR_TOUCHED_NO_TARGET_NO_ORDER
PAPER_DESTINATION_ANCHOR_NOT_TOUCHED
```

## Path states

```text
PAPER_PATH_WAITING_FOR_ENTRY_ANCHOR
PAPER_PATH_HYPOTHETICAL_ENTRY_OPEN_NO_EXIT_TOUCH
PAPER_PATH_DESTINATION_TOUCHED_AFTER_HYPOTHETICAL_ENTRY
PAPER_PATH_INVALIDATION_TOUCHED_AFTER_HYPOTHETICAL_ENTRY
PAPER_PATH_BOTH_DESTINATION_AND_INVALIDATION_TOUCHED_SAME_CLOSE_AMBIGUOUS
```

## Outcomes

```text
PAPER_OUTCOME_WAITING_FOR_ENTRY
PAPER_OUTCOME_HYPOTHETICAL_OPEN
PAPER_OUTCOME_HYPOTHETICAL_DESTINATION
PAPER_OUTCOME_HYPOTHETICAL_INVALIDATION
PAPER_OUTCOME_AMBIGUOUS_SAME_CLOSE_ONLY
```

## Execution safety

Every Phase 18 lifecycle row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE18_LIFECYCLE_ONLY
```

No order is opened, modified, deleted, closed, or sent.

## Design boundary

Phase 18 converts:

```text
Paper Ledger Snapshot
```

into:

```text
Paper Lifecycle Snapshot
```

It is still not a real execution engine.

## Locked boundaries

Phase 18 does not modify:

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

It only reads the Level 19 State Gate paper ledger and the latest closed close value.

## Next natural phase

The next phase can be:

```text
Phase 19 — Paper Result Metrics / R-Equivalent Summary
```

That phase should summarize paper lifecycle rows into dry-run result metrics without enabling real execution.
