# Flag Counting Level 19 — Phase 21 Paper Regime Attribution

## Purpose

Phase 21 adds Paper Regime Attribution above the Phase 20 Paper Portfolio layer.

This phase still does **not** send real orders.

It attributes each paper result row back to the context that produced it:

```text
Hook context
Rally context
MTF alignment context
MTF divergence context
Extreme side
Entry geometry readiness
Entry idea family
Entry decision type
Paper lifecycle path
Paper outcome
Paper result bucket
```

## Hard safety contract

```text
real execution = disabled
paper attribution only
no broker orders
no tickets
no position state
```

## New CSV

Phase 21 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_regime.csv
```

## New input

```text
InpStateGateExportPaperRegimeCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
paper_regime_row_count
paper_regime_status
paper_regime_key
paper_regime_context_family
paper_regime_source_context
paper_regime_mtf_context
paper_regime_geometry_context
paper_regime_outcome
paper_regime_result_bucket
paper_regime_execution_status
paper_regime_notes
```

## Context family examples

```text
REGIME_MTF_ALIGNED_HOOK_EXTREME
REGIME_MTF_DIVERGENT_HOOK_EXTREME
REGIME_HOOK_EXTREME
REGIME_MTF_ALIGNED_RALLY_CONTEXT
REGIME_RALLY_CONTEXT
REGIME_GEOMETRY_CONTEXT
REGIME_CONTEXT_PENDING
```

## Attribution status

Examples:

```text
PAPER_REGIME_ATTRIBUTED_NO_EXECUTION
PAPER_REGIME_ATTRIBUTED_UNKNOWN_RESULT_NO_EXECUTION
PAPER_REGIME_BLOCKED_NO_RESULT_ROW
PAPER_REGIME_BLOCKED_NO_CLOSED_BAR
```

## What the row contains

Each regime attribution row exports:

```text
context_family
source_context
mtf_context
mtf_direction_relation
mtf_side_relation
geometry_context
idea_family
idea_type
decision_type
extreme_source
extreme_side
hook_context
rally_context
lifecycle_path_state
outcome
result_bucket
price_delta
r_status
r_multiple
source_result_key
source_lifecycle_key
source_portfolio_key
attribution_key
execution_status
```

## Design boundary

Phase 21 converts:

```text
Paper Result Metrics
Paper Portfolio Aggregate
State Gate Context
```

into:

```text
Paper Regime Attribution
```

It explains *where* a paper result came from, but it does not approve or execute a trade.

## Locked boundaries

Phase 21 does not modify:

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

It only reads Level 19 State Gate context and paper result rows.

## Next natural phase

The next phase can be:

```text
Phase 22 — Paper Filter Diagnostics
```

That phase should test paper-only filters such as:

```text
only MTF aligned
only Hook source
exclude divergent MTF
exclude ambiguous outcome
require destination anchor
require R-ready row
```

without enabling real execution.
