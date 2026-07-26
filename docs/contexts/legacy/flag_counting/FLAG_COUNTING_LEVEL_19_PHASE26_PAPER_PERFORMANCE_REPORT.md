# Flag Counting Level 19 — Phase 26 Paper Performance Report

## Purpose

Phase 26 adds a paper performance report above the Phase 25 Persistent Paper Trade Lifecycle Engine.

This phase still does **not** send real orders.

It summarizes persistent paper trade lifecycle rows into paper-only performance metrics.

## Hard safety contract

```text
real execution = disabled
paper performance report only
no broker orders
no tickets
no position state
```

## New CSV

Phase 26 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_performance.csv
```

## New input

```text
InpStateGateExportPaperPerformanceCsv = true
```

## Snapshot-level fields

The State Gate snapshot now stores:

```text
paper_performance_row_count
paper_performance_status
paper_performance_key
paper_performance_source_lifecycle_rows
paper_performance_closed_rows
paper_performance_open_rows
paper_performance_pending_entry_rows
paper_performance_blocked_rows
paper_performance_ambiguous_rows
paper_performance_win_rows
paper_performance_loss_rows
paper_performance_r_ready_rows
paper_performance_r_pending_rows
paper_performance_win_rate_like
paper_performance_closed_win_rate_like
paper_performance_net_delta
paper_performance_avg_delta
paper_performance_net_R
paper_performance_avg_R
paper_performance_expectancy_R
paper_performance_best_R
paper_performance_worst_R
paper_performance_distribution
paper_performance_r_distribution
paper_performance_execution_status
paper_performance_notes
```

## Performance status examples

```text
PAPER_PERFORMANCE_EMPTY_NO_EXECUTION
PAPER_PERFORMANCE_HAS_AMBIGUOUS_ROWS_NO_EXECUTION
PAPER_PERFORMANCE_CLOSED_MIXED_NO_EXECUTION
PAPER_PERFORMANCE_CLOSED_WIN_LIKE_ONLY_NO_EXECUTION
PAPER_PERFORMANCE_CLOSED_LOSS_LIKE_ONLY_NO_EXECUTION
PAPER_PERFORMANCE_OPEN_ONLY_OR_OPEN_DOMINANT_NO_EXECUTION
PAPER_PERFORMANCE_PENDING_ENTRY_ONLY_NO_EXECUTION
PAPER_PERFORMANCE_BLOCKED_ONLY_NO_EXECUTION
PAPER_PERFORMANCE_UNKNOWN_NO_EXECUTION
```

## Performance metrics

Phase 26 summarizes:

```text
source_lifecycle_rows
closed_rows
open_rows
pending_entry_rows
blocked_rows
ambiguous_rows
win_rows
loss_rows
r_ready_rows
r_pending_rows
win_rate_like
closed_win_rate_like
net_delta
avg_delta
net_R
avg_R
expectancy_R
best_R
worst_R
distribution
r_distribution
```

## Win/loss definitions

Paper win-like rows are:

```text
PAPER_TRADE_TERMINAL_HIT_DESTINATION
```

Paper loss-like rows are:

```text
PAPER_TRADE_TERMINAL_HIT_INVALIDATION
```

Closed rows are:

```text
win_rows + loss_rows
```

Ambiguous rows are kept separate and do not pretend to be wins or losses.

## R handling

Only rows whose lifecycle `r_status` contains `READY` enter R metrics.

Rows without valid risk distance are counted as:

```text
r_pending_rows
```

This prevents fake precision.

## Execution safety

Every Phase 26 performance row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE26_PERFORMANCE_ONLY
```

No order is opened, modified, deleted, closed, or sent.

## Panel

Phase 26 adds a global panel line:

```text
Performance | status | distribution | avgR
```

## Locked boundaries

Phase 26 does not modify:

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

It only reads persistent paper trade lifecycle rows and writes paper performance diagnostics.

## Next natural phase

The next phase can be:

```text
Phase 27 — Paper MFE / MAE Path Quality
```

That phase should evaluate path smoothness and excursion quality for persistent paper trades without enabling real execution.
