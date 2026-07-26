# Flag Counting Level 19 — Phase 22 Paper Filter Diagnostics

## Purpose

Phase 22 adds paper filter diagnostics above the Phase 21 Paper Regime Attribution layer.

This phase still does **not** send real orders.

It runs diagnostic filters over the current paper regime/result rows and answers:

```text
If this filter had been applied, how many paper rows would remain?
What would the paper result distribution look like?
Would average delta or R-equivalent improve or degrade?
```

## Hard safety contract

```text
real execution = disabled
filter diagnostics only
no broker orders
no tickets
no position state
```

## New CSV

Phase 22 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_filters.csv
```

## New input

```text
InpStateGateExportPaperFiltersCsv = true
```

## Snapshot-level filter fields

The State Gate snapshot now stores:

```text
paper_filter_row_count
paper_filter_status
paper_filter_key
paper_filter_total_filters
paper_filter_active_filters
paper_filter_best_filter
paper_filter_best_distribution
paper_filter_best_avg_delta
paper_filter_best_avg_R
paper_filter_execution_status
paper_filter_notes
```

## Diagnostic filters

Phase 22 evaluates these filter diagnostics:

```text
FILTER_ALL_PAPER_REGIME_ROWS
FILTER_ONLY_MTF_ALIGNED_CONTEXT
FILTER_ONLY_HOOK_EXTREME
FILTER_ONLY_MTF_ALIGNED_HOOK_EXTREME
FILTER_ONLY_GEOMETRY_READY_OR_PARTIAL
FILTER_EXCLUDE_AMBIGUOUS
FILTER_EXCLUDE_WAITING_FOR_ENTRY
FILTER_ONLY_R_READY
FILTER_ONLY_WIN_OR_OPEN_BUCKETS
```

## Each filter row exports

```text
filter_index
filter_name
filter_family
filter_status
filter_rule
rows_before
rows_after
win_like_rows
loss_like_rows
open_rows
waiting_rows
ambiguous_rows
unknown_rows
r_ready_rows
r_pending_rows
net_delta
avg_delta
avg_R
pass_rate
strongest_context
diagnostic_key
execution_status
label
```

## Filter status examples

```text
PAPER_FILTER_NO_SOURCE_ROWS_NO_EXECUTION
PAPER_FILTER_ZERO_ROWS_AFTER_FILTER_NO_EXECUTION
PAPER_FILTER_HAS_AMBIGUOUS_ROWS_NO_EXECUTION
PAPER_FILTER_WIN_LIKE_ONLY_NO_EXECUTION
PAPER_FILTER_LOSS_LIKE_ONLY_NO_EXECUTION
PAPER_FILTER_HAS_OPEN_ROWS_NO_EXECUTION
PAPER_FILTER_MIXED_DIAGNOSTIC_NO_EXECUTION
```

## Design boundary

Phase 22 does not decide real entries.

It does not say:

```text
trade this
buy
sell
send order
allow execution
```

It only compares diagnostic filter scenarios.

## Execution safety

Every Phase 22 row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE22_FILTER_ONLY
```

## Locked boundaries

Phase 22 does not modify:

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

It only reads paper regime/result rows and exports filter diagnostics.

## Next natural phase

The next phase can be:

```text
Phase 23 — Dry-Run Decision Policy
```

That phase should use the best diagnostic filters to create a dry-run policy gate, still with real execution disabled.
