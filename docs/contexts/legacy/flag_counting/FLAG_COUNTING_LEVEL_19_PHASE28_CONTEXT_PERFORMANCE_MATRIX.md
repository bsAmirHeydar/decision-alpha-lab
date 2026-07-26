# Flag Counting Level 19 — Phase 28 Context Performance Matrix

## Purpose

Phase 28 adds a context performance matrix above the Phase 27 Paper MFE / MAE Path Quality layer.

This phase still does **not** send real orders.

It groups paper regime, paper result, and path quality data by context dimensions so the project can compare which families of context look better or worse.

## Hard safety contract

```text
real execution = disabled
context matrix only
no broker orders
no tickets
no position state
```

## New CSV

Phase 28 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_context_performance.csv
```

## New input

```text
InpStateGateExportContextPerformanceCsv = true
```

## Snapshot-level fields

The State Gate snapshot now stores:

```text
context_performance_row_count
context_performance_status
context_performance_key
context_performance_total_rows
context_performance_active_rows
context_performance_best_context
context_performance_best_dimension
context_performance_best_avg_R
context_performance_best_smoothness
context_performance_distribution
context_performance_execution_status
context_performance_notes
```

## Matrix dimensions

Phase 28 evaluates these context dimensions:

```text
ALL_CONTEXT
MTF_ALIGNED_CONTEXT
HOOK_CONTEXT
MTF_ALIGNED_HOOK_CONTEXT
RALLY_CONTEXT
GEOMETRY_READY_OR_PARTIAL
R_READY_CONTEXT
CLEAN_PATH_CONTEXT
ADVERSE_PATH_CONTEXT
AMBIGUOUS_CONTEXT
```

## Row-level metrics

Each context matrix row exports:

```text
dimension_name
dimension_value
matrix_status
context_rule
source_regime_rows
rows_after
win_like_rows
loss_like_rows
open_rows
waiting_rows
ambiguous_rows
unknown_rows
r_ready_rows
r_pending_rows
clean_path_rows
adverse_path_rows
pending_path_rows
ambiguous_path_rows
net_delta
avg_delta
net_R
avg_R
avg_mfe_R
avg_mae_R
avg_smoothness_score
win_rate_like
pass_rate
distribution
context_performance_key
execution_status
label
```

## Matrix status examples

```text
CONTEXT_PERFORMANCE_NO_SOURCE_ROWS_NO_EXECUTION
CONTEXT_PERFORMANCE_ZERO_ROWS_AFTER_CONTEXT_NO_EXECUTION
CONTEXT_PERFORMANCE_HAS_AMBIGUOUS_ROWS_NO_EXECUTION
CONTEXT_PERFORMANCE_POSITIVE_R_CLEAN_PATH_NO_EXECUTION
CONTEXT_PERFORMANCE_POSITIVE_R_NO_EXECUTION
CONTEXT_PERFORMANCE_NEGATIVE_R_NO_EXECUTION
CONTEXT_PERFORMANCE_OPEN_OR_PENDING_NO_EXECUTION
CONTEXT_PERFORMANCE_NEUTRAL_OR_UNKNOWN_NO_EXECUTION
```

## Why this matters

Phase 28 starts answering:

```text
Which context family has better paper behavior?
Which contexts produce positive R-like outcomes?
Which contexts are cleaner by path quality?
Which contexts are adverse or ambiguous?
```

It helps move the project from raw paper tracking into context-aware edge diagnosis.

## Important limitation

The matrix is still based on the current State Gate snapshot.

It is not yet a long-history database report.

## Execution safety

Every Phase 28 row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE28_CONTEXT_MATRIX_ONLY
```

No order is opened, modified, deleted, closed, or sent.

## Locked boundaries

Phase 28 does not modify:

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

It only reads paper regime, result, performance, and path-quality context.

## Next natural phase

The next phase can be:

```text
Phase 29 — Policy Refinement from Context Matrix
```

That phase should use the context matrix to refine the dry-run policy gate without enabling real execution.
