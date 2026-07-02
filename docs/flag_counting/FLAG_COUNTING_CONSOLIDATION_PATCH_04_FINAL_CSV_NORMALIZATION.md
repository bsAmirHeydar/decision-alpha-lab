# Flag Counting — Consolidation Patch 04 / Final CSV Field Normalization

## Purpose

This patch is not a new feature level.

It does not add Level 31.

It does not add execution.

It adds a machine-friendly normalized CSV snapshot derived from the final no-send decision state.

Consolidation Patch 02 created a human-readable final decision file.

Consolidation Patch 04 creates a cleaner version for Excel, Python, dashboards, and automated reports.

## New output

```text
MQL5/Files/FlagCountingPhoenix/final_no_send_decision_state_normalized.csv
```

This is a latest-state snapshot.

It is not an append ledger.

## New inputs

```text
InpConsolidation04FinalCsvNormalizationEnabled = true
InpConsolidation04FinalCsvNormalizationExportCsv = true
InpConsolidation04FinalCsvNormalizationPrintSummary = false
InpConsolidation04FinalCsvNormalizationWriteLatestCsv = true
InpConsolidation04FinalCsvNormalizationRequireNoSendIntegrity = true
InpConsolidation04FinalCsvNormalizationFolder = "FlagCountingPhoenix"
```

## What is normalized

The normalized CSV uses:

```text
stable schema version
stable column names
integer boolean flags
separate state fields
separate blocker fields
separate request id fields
separate price fields
separate risk/reward fields
separate lifecycle fields
```

## Boolean columns

Boolean fields are exported as integers:

```text
1 = true
0 = false
```

Examples:

```text
decision_ready_i
context_ready_i
no_send_integrity_i
entry_bridge_ready_i
paper_intent_allowed_i
safety_gate_passed_i
dry_run_request_built_i
validator_passed_i
audit_passed_i
adapter_registered_i
lifecycle_tracked_i
```

## Direction columns

Direction is exported as both text and sign:

```text
direction_label
direction_sign
```

Values:

```text
DIRECTION_BULLISH -> 1
DIRECTION_BEARISH -> -1
unknown -> 0
```

## Risk/reward columns

The normalized file adds:

```text
risk_distance
reward_distance
rr_like
```

These are derived from:

```text
entry_price
stop_price
target_price
```

## No-send integrity

The normalized file preserves the no-send integrity check.

If no-send integrity is broken and the requirement is enabled, the row is marked:

```text
FINAL_CSV_NORMALIZED_BLOCKED
BLOCK_NORMALIZED_NO_SEND_INTEGRITY_BROKEN
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
normalization snapshot only
no send
no broker
no execution
```

## Next correct patch

The next patch should be a compile-fix if MetaEditor reports errors.

If compile is clean, the next engineering patch can be:

```text
Consolidation Patch 05 — Runtime Health Summary
```

That patch should summarize whether all expected CSV outputs are enabled and internally coherent, without adding trading behavior.
