# Flag Counting — Consolidation Patch 05 / Runtime Health Summary

## Purpose

This patch is not a new feature level.

It does not add Level 31.

It does not add execution.

It adds a runtime health summary for the existing no-send research stack.

The goal is to know quickly whether the no-send stack is operational, export-enabled, coherent, and safe.

## New output

```text
MQL5/Files/FlagCountingPhoenix/runtime_no_send_health_summary.csv
```

This is a latest-state snapshot.

It is not an append ledger.

## New inputs

```text
InpConsolidation05RuntimeHealthEnabled = true
InpConsolidation05RuntimeHealthExportCsv = true
InpConsolidation05RuntimeHealthPrintSummary = false
InpConsolidation05RuntimeHealthWriteLatestCsv = true
InpConsolidation05RuntimeHealthRequireContextReady = false
InpConsolidation05RuntimeHealthRequireFinalDecisionExport = true
InpConsolidation05RuntimeHealthRequireNormalizedExport = true
InpConsolidation05RuntimeHealthRequireNoSendIntegrity = true
InpConsolidation05RuntimeHealthFolder = "FlagCountingPhoenix"
```

## What it summarizes

The runtime health row summarizes:

```text
context enabled
context export enabled
context ready
context status
final decision enabled
final decision export enabled
final decision ready
final decision state
normalized export enabled
normalized quality status
no-send integrity
expected outputs enabled
setup state
chain stage
blocker layer
blocker reason
request id
virtual ticket
direction
entry
SL
TP
request volume
realized R-like
```

## Health statuses

```text
RUNTIME_HEALTH_OK_NO_SEND
RUNTIME_HEALTH_WARN_NO_SEND
RUNTIME_HEALTH_BLOCKED_NO_SEND
```

## Block reasons

```text
BLOCK_RUNTIME_NO_SEND_INTEGRITY_BROKEN
BLOCK_RUNTIME_CONTEXT_NOT_READY
BLOCK_RUNTIME_FINAL_DECISION_EXPORT_DISABLED
BLOCK_RUNTIME_NORMALIZED_EXPORT_DISABLED
WARN_RUNTIME_FINAL_DECISION_BLOCKED:<reason>
WARN_RUNTIME_NORMALIZED_BLOCKED:<reason>
```

## Why warnings are not hard failures

A blocked setup is not necessarily a broken system.

For example, a setup can be blocked by Safety Gate or Validator while the runtime stack is still working correctly.

That is why final-decision blocks become runtime warnings, not runtime failures.

True runtime failures are reserved for things such as:

```text
no-send integrity broken
required exports disabled
context required but unavailable
```

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
health snapshot only
no send
no broker
no execution
```

## Next correct patch

The next patch should be a compile-fix if MetaEditor reports errors.

If compile is clean, the next engineering patch can be:

```text
Consolidation Patch 06 — Documentation and Usage Playbook
```

That patch should focus on how to read the CSV stack and how to use the final decision outputs, without adding trading behavior.
