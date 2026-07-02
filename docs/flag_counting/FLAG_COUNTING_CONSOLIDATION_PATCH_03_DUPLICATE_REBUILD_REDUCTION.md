# Flag Counting — Consolidation Patch 03 / Duplicate Rebuild Reduction

## Purpose

This patch is not a new feature level.

It does not add Level 31.

It does not add execution.

It reduces repeated internal rebuilds in the no-send chain by reusing the latest-row caches introduced in Consolidation Patch 01.

## Problem before this patch

The no-send chain was correct but repetitive.

For example:

```text
Level 25 built dry-run from Entry Bridge, Paper Intent, and Safety Gate.
Level 26 rebuilt Entry Bridge, Paper Intent, Safety Gate, and Dry Run again.
Level 27 rebuilt the same chain again.
Level 28 rebuilt the same chain again.
Level 29 rebuilt the same chain again.
Level 30 rebuilt the same chain again.
```

That was safe, but heavy and noisy.

It also meant some internal dedupe counters could be touched more often than necessary.

## What changed

The engines now prefer cached rows when available.

```text
Level 26 prefers Level 25 dry-run cache.
Level 27 prefers Level 21, 24, 25, and 26 caches.
Level 28 prefers Level 21, 24, 25, and 26 caches.
Level 29 prefers Level 25, 26, and 28 caches.
Level 30 prefers Level 29 adapter cache.
```

If a required cache is missing, the engine falls back to the previous rebuild path.

## Fallback behavior

Fallback is preserved intentionally.

This means the modules still work if a previous layer is disabled or has not run.

The fallback rebuild path also refreshes the relevant context caches so Consolidation Patch 01 and Patch 02 continue to have the latest available state.

## Outputs preserved

This patch preserves the existing outputs:

```text
state_gate_level26_broker_validator.csv
state_gate_level27_broker_request_ledger.csv
latest_state_gate_level27_broker_request_ledger.csv
state_gate_level28_broker_request_audit.csv
latest_state_gate_level28_broker_request_audit.csv
state_gate_level29_paper_broker_adapter.csv
latest_state_gate_level29_paper_broker_adapter.csv
state_gate_level30_paper_broker_lifecycle.csv
latest_state_gate_level30_paper_broker_lifecycle.csv
latest_consolidation_01_no_send_context.csv
final_no_send_decision_state.csv
```

## Context-cache fix

This patch also ensures Level 27 through Level 30 update their Consolidation Patch 01 latest-row caches after rows are built.

That keeps:

```text
latest_consolidation_01_no_send_context.csv
final_no_send_decision_state.csv
```

aligned with the actual latest no-send chain state.

## Hard boundary

This patch does not add:

```text
OrderSend
OrderCheck
CTrade
broker request
real order
real position
volume sizing
risk sizing
real execution
renderer mutation
chart-object mutation
```

It remains:

```text
CSV-only
read-only
panel off
print silent by default
cache-first where safe
fallback rebuild where necessary
no send
no broker
no execution
```

## Next correct patch

The next patch should be a compile-fix if MetaEditor reports errors.

If compile is clean, the next engineering patch can be:

```text
Consolidation Patch 04 — Final CSV Field Normalization
```

That patch should make the final CSV outputs easier to consume in Excel/Python without changing trading behavior.
