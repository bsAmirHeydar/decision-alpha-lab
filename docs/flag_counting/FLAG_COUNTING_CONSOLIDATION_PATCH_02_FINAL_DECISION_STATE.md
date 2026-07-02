# Flag Counting — Consolidation Patch 02 / Final No-Send Decision State

## Purpose

This patch is not a new feature level.

It does not add Level 31.

It does not add execution.

It adds a final human-readable decision/dashboard snapshot from the Consolidation Patch 01 no-send context.

The goal is to avoid manually reading many CSV files when you only need the final state of the no-send research chain.

## New output

```text
MQL5/Files/FlagCountingPhoenix/final_no_send_decision_state.csv
```

This is a latest-state snapshot.

It is not an append ledger.

## New inputs

```text
InpConsolidation02FinalDecisionEnabled = true
InpConsolidation02FinalDecisionExportCsv = true
InpConsolidation02FinalDecisionPrintSummary = false
InpConsolidation02FinalDecisionWriteLatestCsv = true
InpConsolidation02FinalDecisionRequireContextReady = true
InpConsolidation02FinalDecisionRequireLifecycleTracked = false
InpConsolidation02FinalDecisionRequireNoSendIntegrity = true
InpConsolidation02FinalDecisionFolder = "FlagCountingPhoenix"
```

## What it summarizes

The final decision row summarizes:

```text
decision_ready
decision_state
decision_block_reason
setup_state
chain_stage
next_action_hint
context status
entry bridge ready
paper intent allowed
safety gate passed
dry-run request built
validator passed
audit passed
adapter registered
lifecycle tracked
request id
request key
virtual ticket
direction
entry
SL
TP
volume
lifecycle status
paper order state
realized R-like
blocker layer
blocker reason
no-send integrity
```

## Decision states

```text
FINAL_DECISION_READY_NO_SEND
FINAL_DECISION_BLOCKED_NO_SEND
```

## Setup states

```text
SETUP_BLOCKED
SETUP_READY_NO_SEND
SETUP_PAPER_TARGET_HIT
SETUP_PAPER_STOP_HIT
SETUP_PAPER_ACTIVE_OPEN
SETUP_PAPER_ENTERED
SETUP_PAPER_EXPIRED
SETUP_PAPER_TRACKED
```

## Chain stages

```text
CHAIN_BLOCKED_AT_ENTRY_BRIDGE
CHAIN_BLOCKED_AT_PAPER_INTENT
CHAIN_BLOCKED_AT_SAFETY_GATE
CHAIN_BLOCKED_AT_DRY_RUN
CHAIN_BLOCKED_AT_VALIDATOR
CHAIN_BLOCKED_AT_AUDIT
CHAIN_BLOCKED_AT_ADAPTER
CHAIN_BLOCKED_AT_LIFECYCLE
CHAIN_LIFECYCLE_TRACKED
CHAIN_READY_NO_SEND
```

## Blocker logic

The final decision snapshot identifies the first blocking layer in this order:

```text
Level 20 Entry Bridge
Level 21 Paper Intent
Level 24 Safety Gate
Level 25 Broker Dry Run
Level 26 Broker Validator
Level 28 Broker Request Audit
Level 29 Paper Broker Adapter
Level 30 Paper Broker Lifecycle
```

## No-send integrity

The decision snapshot requires:

```text
NO_ORDER_SEND
NO_ORDER_CHECK
NO_CTRADE
request_volume == 0.0
```

If no-send integrity breaks, the final decision blocks with:

```text
BLOCK_FINAL_NO_SEND_INTEGRITY_BROKEN
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
dashboard snapshot only
no send
no broker
no execution
```

## Next correct patch

The next patch should only be a compile-fix if MetaEditor reports errors.

If compile is clean, the next engineering patch can be:

```text
Consolidation Patch 03 — Duplicate Rebuild Reduction
```

That patch should carefully begin replacing repeated internal rebuilds with shared cached context where safe.
