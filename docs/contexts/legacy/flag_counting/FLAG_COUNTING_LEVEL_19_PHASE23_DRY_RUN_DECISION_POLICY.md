# Flag Counting Level 19 — Phase 23 Dry-Run Decision Policy

## Purpose

Phase 23 adds a dry-run decision policy above the Phase 22 Paper Filter Diagnostics layer.

This phase still does **not** send real orders.

It converts paper regime attribution and filter diagnostics into a policy gate that can allow or block a **dry-run only** decision.

## Hard safety contract

```text
real execution = disabled
dry-run policy only
no broker orders
no tickets
no position state
```

The policy can allow a dry-run row, but it never enables real execution.

## New CSV

Phase 23 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_paper_policy.csv
```

## New input

```text
InpStateGateExportPaperPolicyCsv = true
```

## New per-timeframe fields

Each State Gate timeframe state now stores:

```text
paper_policy_row_count
paper_policy_status
paper_policy_key
paper_policy_name
paper_policy_family
paper_policy_allowed_dry_run
paper_policy_score
paper_policy_score_status
paper_policy_block_reason
paper_policy_required_context
paper_policy_source_filter
paper_policy_execution_status
paper_policy_notes
```

## New snapshot-level fields

The State Gate snapshot now stores:

```text
paper_policy_row_count
paper_policy_status
paper_policy_key
paper_policy_total_rows
paper_policy_allowed_dry_run_rows
paper_policy_blocked_rows
paper_policy_best_policy
paper_policy_best_score
paper_policy_distribution
paper_policy_execution_status
paper_policy_notes
```

## Policy names

Examples:

```text
POLICY_DRY_RUN_MTF_ALIGNED_HOOK_EXTREME
POLICY_DRY_RUN_HOOK_EXTREME
POLICY_DRY_RUN_MTF_ALIGNED_RALLY_CONTEXT
POLICY_DRY_RUN_GEOMETRY_READY_OR_PARTIAL
POLICY_DRY_RUN_CONTEXT_REVIEW
```

## Policy score

The score is diagnostic and paper-only.

It rewards:

```text
MTF-aligned Hook context
Hook context
MTF-aligned Rally context
Geometry ready or partial context
Win-like or open paper result buckets
R-ready rows
Positive R-equivalent values
Best filter agreement
```

It penalizes:

```text
loss-like paper result buckets
ambiguous paper rows
waiting-for-entry rows
negative R-equivalent values
```

The score is capped to:

```text
0 <= policy_score <= 100
```

## Policy block reasons

Examples:

```text
POLICY_BLOCK_NO_CLOSED_BAR
POLICY_BLOCK_NO_REGIME_ATTRIBUTION
POLICY_BLOCK_AMBIGUOUS_PAPER_RESULT
POLICY_BLOCK_WAITING_FOR_ENTRY
POLICY_BLOCK_SCORE_BELOW_DRY_RUN_THRESHOLD
POLICY_ALLOW_DRY_RUN_CONTEXT_ONLY_NO_REAL_EXECUTION
```

## Policy status

Examples:

```text
PAPER_POLICY_ALLOWED_DRY_RUN_NO_REAL_EXECUTION
PAPER_POLICY_BLOCKED_NO_REGIME_NO_EXECUTION
PAPER_POLICY_BLOCKED_AMBIGUOUS_NO_EXECUTION
PAPER_POLICY_BLOCKED_WAITING_NO_EXECUTION
PAPER_POLICY_BLOCKED_LOW_SCORE_NO_EXECUTION
PAPER_POLICY_BLOCKED_NO_EXECUTION
```

## Design boundary

Phase 23 is the first policy gate, but it is deliberately not an execution gate.

It does not say:

```text
send order
open position
place limit order
place market order
real entry allowed
```

It only says whether a context is worth a dry-run policy row.

## Execution safety

Every Phase 23 policy row keeps:

```text
execution_status = REAL_EXECUTION_DISABLED_PHASE23_POLICY_ONLY
```

## Locked boundaries

Phase 23 does not modify:

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

It only reads paper regime, paper result, paper portfolio, and filter diagnostic context.

## Next natural phase

The next phase can be:

```text
Phase 24 — Persistent Paper Trade Ledger
```

That phase should persist paper trades across closed bars while keeping real execution disabled.
