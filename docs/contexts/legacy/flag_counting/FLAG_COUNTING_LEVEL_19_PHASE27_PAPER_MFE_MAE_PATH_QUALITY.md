# Flag Counting Level 19 — Phase 27 Paper MFE / MAE Path Quality

## Purpose

Phase 27 adds paper MFE / MAE path quality diagnostics above the Phase 26 Paper Performance Report.

This phase still does **not** send real orders.

It evaluates persistent paper trade lifecycle rows and produces close-only path quality metrics:

```text
favorable excursion proxy
adverse excursion proxy
MFE proxy
MAE proxy
MFE in R
MAE in R
net R
path smoothness score
pullback pressure status
path quality bucket
```

## Hard safety contract

```text
real execution = disabled
paper path quality only
no broker orders
no tickets
no position state
```

## New CSV

Phase 27 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_path_quality.csv
```

## New input

```text
InpStateGateExportPaperPathQualityCsv = true
```

## Snapshot-level fields

The State Gate snapshot now stores:

```text
paper_path_quality_row_count
paper_path_quality_status
paper_path_quality_key
paper_path_quality_total_rows
paper_path_quality_clean_rows
paper_path_quality_adverse_rows
paper_path_quality_pending_rows
paper_path_quality_blocked_rows
paper_path_quality_ambiguous_rows
paper_path_quality_r_ready_rows
paper_path_quality_r_pending_rows
paper_path_quality_avg_mfe_R
paper_path_quality_avg_mae_R
paper_path_quality_avg_net_R
paper_path_quality_best_mfe_R
paper_path_quality_worst_mae_R
paper_path_quality_avg_smoothness_score
paper_path_quality_distribution
paper_path_quality_execution_status
paper_path_quality_notes
```

## Row-level metrics

Each row exports:

```text
trade_id
direction
terminal_status
lifecycle_status
entry_price
current_close
destination_price
invalidation_price
signed_delta
risk_distance
favorable_delta
adverse_delta
mfe_proxy
mae_proxy
mfe_R
mae_R
net_R
path_smoothness_score
pullback_pressure_status
path_quality_bucket
path_quality_status
```

## Important limitation

Phase 27 is still close-only.

It does **not** yet use intrabar high/low over the full path.

So the values are deliberately named:

```text
MFE proxy
MAE proxy
```

The goal is not fake precision. The goal is to begin measuring path quality in a conservative, audit-friendly way.

## Buckets

Examples:

```text
PAPER_PATH_BUCKET_CLEAN_POSITIVE_R
PAPER_PATH_BUCKET_ACCEPTABLE_POSITIVE_R
PAPER_PATH_BUCKET_POSITIVE_WITH_PULLBACK
PAPER_PATH_BUCKET_FLAT_OR_NO_R
PAPER_PATH_BUCKET_ADVERSE
PAPER_PATH_BUCKET_PENDING_ENTRY
PAPER_PATH_BUCKET_AMBIGUOUS
PAPER_PATH_BUCKET_BLOCKED
```

## Pullback pressure statuses

Examples:

```text
PAPER_PULLBACK_PRESSURE_CLEAN_CLOSE_ONLY
PAPER_PULLBACK_PRESSURE_LOW_RELATIVE_TO_MFE
PAPER_PULLBACK_PRESSURE_MEDIUM_RELATIVE_TO_MFE
PAPER_PULLBACK_PRESSURE_HIGH_RELATIVE_TO_MFE
PAPER_PULLBACK_PRESSURE_ADVERSE_ONLY_CLOSE_ONLY
PAPER_PULLBACK_PRESSURE_PENDING_ENTRY
PAPER_PULLBACK_PRESSURE_AMBIGUOUS
PAPER_PULLBACK_PRESSURE_BLOCKED
```

## Why this matters

This phase supports the project objective of measuring path cleanliness, not only final outcome.

It starts answering:

```text
Did the paper setup move cleanly?
Did it need a lot of adverse movement?
Was the positive path smooth or painful?
Was the open state actually favorable or adverse?
```

## Execution safety

Every Phase 27 row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE27_PATH_QUALITY_ONLY
```

No order is opened, modified, deleted, closed, or sent.

## Locked boundaries

Phase 27 does not modify:

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

It only reads persistent paper trade lifecycle rows and writes paper path quality diagnostics.

## Next natural phase

The next phase can be:

```text
Phase 28 — Context Performance Matrix
```

That phase should group paper performance and path quality by context family, timeframe, MTF alignment, Hook/Rally source, and geometry readiness without enabling real execution.
