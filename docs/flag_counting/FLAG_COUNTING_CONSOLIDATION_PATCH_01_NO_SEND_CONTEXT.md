# Flag Counting — Consolidation Patch 01 / No-Send Context

## Purpose

This patch is not a new feature level.

It does not add Level 31.

It does not add execution.

It adds a shared no-send context snapshot for the existing Level 20-30 research chain.

Before this patch, each layer from Level 25 onward rebuilt parts of the no-send chain internally.

This patch starts the consolidation process by caching the latest rows produced by the existing engines and exporting one unified latest context row.

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
context-only
no send
no broker
no execution
```

## New output

```text
MQL5/Files/FlagCountingPhoenix/latest_consolidation_01_no_send_context.csv
```

This file is not an append ledger.

It is a latest-state context snapshot.

## New inputs

```text
InpConsolidation01NoSendContextEnabled = true
InpConsolidation01NoSendContextExportCsv = true
InpConsolidation01NoSendContextPrintSummary = false
InpConsolidation01NoSendContextWriteLatestCsv = true
InpConsolidation01NoSendContextFolder = "FlagCountingPhoenix"
```

## What gets consolidated

The context snapshot reads latest-row caches from:

```text
Level 20 Entry Bridge
Level 21 Paper Intent
Level 24 Safety Gate
Level 25 Broker Dry Run
Level 26 Broker Validator
Level 27 Broker Request Ledger
Level 28 Broker Request Audit
Level 29 Paper Broker Adapter
Level 30 Paper Broker Lifecycle
```

## Cached rows

This patch adds latest-row caches to the no-send engines:

```text
g_fp_c01_l20_entry_bridge_row
g_fp_c01_l21_paper_intent_row
g_fp_c01_l24_safety_gate_row
g_fp_c01_l25_dry_run_row
g_fp_c01_l26_validator_row
g_fp_c01_l27_ledger_row
g_fp_c01_l28_audit_row
g_fp_c01_l29_adapter_row
g_fp_c01_l30_lifecycle_row
```

Each cache also has a `has_*` flag.

The cache is diagnostic only.

It does not alter trading behavior.

## Context statuses

```text
NO_SEND_CONTEXT_READY
NO_SEND_CONTEXT_INCOMPLETE
```

## Context block reasons

```text
BLOCK_CONTEXT_NO_ENTRY_BRIDGE_CACHE
BLOCK_CONTEXT_NO_PAPER_INTENT_CACHE
BLOCK_CONTEXT_NO_SAFETY_GATE_CACHE
BLOCK_CONTEXT_NO_DRY_RUN_CACHE
BLOCK_CONTEXT_NO_VALIDATOR_CACHE
BLOCK_CONTEXT_NO_AUDIT_CACHE
BLOCK_CONTEXT_NO_ADAPTER_CACHE
BLOCK_CONTEXT_NO_LIFECYCLE_CACHE
```

## Why this is the correct consolidation first step

A full refactor would immediately replace the internal rebuilds in Level 25-30.

That would be riskier.

This patch takes the safer path:

```text
1. Preserve all current engine outputs.
2. Add latest-row caches.
3. Export one shared context snapshot.
4. Keep execution disabled.
5. Prepare the codebase for a later low-risk refactor where engines can consume the shared context directly.
```

## Next correct patch

The next patch should be:

```text
Consolidation Patch 02 — Context-Driven Export Routing
```

That patch can start routing selected outputs from the shared context instead of rebuilding the same chain repeatedly.

It should still avoid OrderSend, OrderCheck, CTrade, broker requests, real execution, volume sizing, and risk sizing.
