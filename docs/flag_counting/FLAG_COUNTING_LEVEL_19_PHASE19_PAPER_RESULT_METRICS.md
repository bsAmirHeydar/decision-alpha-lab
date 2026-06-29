# Flag Counting Level 19 — Phase 19 Paper Result Metrics / R-Equivalent Summary

## Purpose

Phase 19 adds paper result metrics above the Phase 18 Paper Lifecycle layer.

This phase still does **not** send real orders and does **not** create real broker-side performance state.

It summarizes each paper lifecycle row into a paper result row:

```text
paper outcome
paper result bucket
signed price delta
absolute distance
R-equivalent status
R-equivalent value when possible
```

## Hard safety contract

```text
real execution = disabled
paper result only
no broker orders
no tickets
no position state
```

## New CSV

Phase 19 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_results.csv
```

## New input

```text
InpStateGateExportPaperResultsCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
paper_result_row_count
paper_result_status
paper_result_key
paper_result_outcome
paper_result_direction
paper_result_type
paper_result_entry_price
paper_result_exit_anchor_price
paper_result_price_delta
paper_result_abs_distance
paper_result_r_status
paper_result_r_multiple
paper_result_bucket
paper_result_execution_status
paper_result_notes
```

## Result buckets

Examples:

```text
PAPER_RESULT_BUCKET_HYPOTHETICAL_WIN
PAPER_RESULT_BUCKET_HYPOTHETICAL_LOSS
PAPER_RESULT_BUCKET_HYPOTHETICAL_OPEN
PAPER_RESULT_BUCKET_AMBIGUOUS
PAPER_RESULT_BUCKET_WAITING
PAPER_RESULT_BUCKET_UNKNOWN
```

## Result status

Examples:

```text
PAPER_RESULT_HYPOTHETICAL_WIN_NO_EXECUTION
PAPER_RESULT_HYPOTHETICAL_LOSS_NO_EXECUTION
PAPER_RESULT_HYPOTHETICAL_OPEN_NO_EXECUTION
PAPER_RESULT_AMBIGUOUS_CLOSE_ONLY_NO_EXECUTION
PAPER_RESULT_WAITING_FOR_ENTRY_NO_EXECUTION
PAPER_RESULT_UNKNOWN_NO_EXECUTION
```

## Distance logic

For a hypothetical destination outcome:

```text
price_delta = abs(destination_price - entry_price)
```

For a hypothetical invalidation outcome:

```text
price_delta = -abs(entry_price - invalidation_price)
```

For a still-open paper state:

```text
BUY:  price_delta = last_closed_close - entry_price
SELL: price_delta = entry_price - last_closed_close
```

## R-equivalent status

Phase 19 can only compute an R multiple when a non-zero invalidation distance exists:

```text
risk = abs(entry_price - invalidation_price)
R    = price_delta / risk
```

When invalidation is still only an anchor or has no buffer distance, the row stays:

```text
PAPER_R_PENDING_INVALIDATION_BUFFER_NO_RISK_DISTANCE
```

This is intentional. It prevents fake precision.

## Execution safety

Every Phase 19 result row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE19_RESULT_ONLY
```

No order is opened, modified, deleted, closed, or sent.

## Design boundary

Phase 19 converts:

```text
Paper Lifecycle Snapshot
```

into:

```text
Paper Result Metrics Snapshot
```

It is still not a real execution engine.

## Locked boundaries

Phase 19 does not modify:

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

It only reads the Level 19 State Gate paper lifecycle context.

## Next natural phase

The next phase can be:

```text
Phase 20 — Paper Portfolio / Aggregate Metrics
```

That phase should aggregate paper result rows across the three State Gate timeframes without enabling real execution.
