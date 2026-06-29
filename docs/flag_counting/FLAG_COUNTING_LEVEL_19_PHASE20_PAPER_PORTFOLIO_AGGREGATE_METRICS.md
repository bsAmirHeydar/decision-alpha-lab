# Flag Counting Level 19 — Phase 20 Paper Portfolio / Aggregate Metrics

## Purpose

Phase 20 adds paper portfolio aggregation above the Phase 19 Paper Result Metrics layer.

This phase still does **not** send real orders and does **not** create broker-side positions.

It summarizes all paper result rows in the current State Gate snapshot into one portfolio-level row.

## Hard safety contract

```text
real execution = disabled
paper portfolio only
no broker orders
no tickets
no position state
```

## New CSV

Phase 20 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_portfolio.csv
```

## New input

```text
InpStateGateExportPaperPortfolioCsv = true
```

## Snapshot-level portfolio fields

The State Gate snapshot now stores:

```text
paper_portfolio_row_count
paper_portfolio_status
paper_portfolio_key
paper_portfolio_total_results
paper_portfolio_win_like_rows
paper_portfolio_loss_like_rows
paper_portfolio_open_rows
paper_portfolio_waiting_rows
paper_portfolio_ambiguous_rows
paper_portfolio_unknown_rows
paper_portfolio_r_ready_rows
paper_portfolio_r_pending_rows
paper_portfolio_net_delta
paper_portfolio_avg_delta
paper_portfolio_avg_R
paper_portfolio_best_R
paper_portfolio_worst_R
paper_portfolio_distribution
paper_portfolio_execution_status
paper_portfolio_notes
```

## Portfolio status examples

```text
PAPER_PORTFOLIO_EMPTY_NO_EXECUTION
PAPER_PORTFOLIO_HAS_AMBIGUOUS_ROWS_NO_EXECUTION
PAPER_PORTFOLIO_HAS_OPEN_ROWS_NO_EXECUTION
PAPER_PORTFOLIO_WAITING_ONLY_NO_EXECUTION
PAPER_PORTFOLIO_WIN_LIKE_ONLY_NO_EXECUTION
PAPER_PORTFOLIO_LOSS_LIKE_ONLY_NO_EXECUTION
PAPER_PORTFOLIO_MIXED_RESULT_ROWS_NO_EXECUTION
```

## Aggregate metrics

Phase 20 aggregates:

```text
total_result_rows
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
best_R
worst_R
result_distribution
```

## R handling

R is only aggregated for paper result rows whose `r_status` contains `READY`.

Rows with pending risk geometry are counted separately:

```text
r_pending_rows
```

This keeps the portfolio summary honest and prevents fake R precision.

## Panel and panel-line visibility

Phase 20 adds a global portfolio line to the State Gate panel and to:

```text
latest_state_gate_panel_lines.csv
```

The panel line summarizes:

```text
portfolio_status
result_distribution
net_delta
avg_R
```

## Execution safety

Every Phase 20 portfolio row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE20_PORTFOLIO_ONLY
```

No order is opened, modified, deleted, closed, or sent.

## Locked boundaries

Phase 20 does not modify:

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

It only reads the Level 19 State Gate paper result rows and aggregates them.

## Next natural phase

The next phase can be:

```text
Phase 21 — Paper Regime Attribution
```

That phase should attribute paper results back to their context:

```text
Hook source
Rally source
MTF alignment
MTF divergence
LOW_EXTREME
HIGH_EXTREME
geometry ready / partial
idea family
decision type
```

This is where the research starts identifying which contexts are worth keeping.
