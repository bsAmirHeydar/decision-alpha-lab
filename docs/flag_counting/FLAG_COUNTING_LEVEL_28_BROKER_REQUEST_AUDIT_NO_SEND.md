# Flag Counting Level 28 — Broker Request Audit / No Send

## Purpose

Level 28 audits the no-send broker request chain after Level 27.

Level 25 builds the dry-run preview.

Level 26 validates the preview.

Level 27 records the preview and validator result into a ledger.

Level 28 audits whether the chain is internally coherent and still respects the no-send contract.

This is still not execution.

It does not call `OrderSend`.

It does not call `OrderCheck`.

It does not use `CTrade`.

It does not create a broker request.

It does not create a position.

It does not calculate volume or account risk.

## Hard boundary

Level 28 does not modify:

```text
FP_Renderer.mqh
FP_RenderRules.mqh
FP_RenderTypes.mqh
F / Hook / Node detection logic
curve drawing logic
line drawing logic
RTV / zone objects
chart objects
license logic
real execution logic
```

It remains:

```text
CSV-only
read-only
panel off
print silent by default
audit-only
no OrderSend
no OrderCheck
no CTrade
no position
no volume sizing
no risk sizing
no real execution
```

## New outputs

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level28_broker_request_audit.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_level28_broker_request_audit.csv
```

The first file is append-only.

The second file is the latest snapshot.

## New inputs

```text
InpLevel28BrokerRequestAuditEnabled = true
InpLevel28BrokerRequestAuditExportCsv = true
InpLevel28BrokerRequestAuditPrintSummary = false
InpLevel28BrokerRequestAuditAppendCsv = true
InpLevel28BrokerRequestAuditWriteLatestCsv = true
InpLevel28BrokerRequestAuditSkipDuplicateAuditKey = true
InpLevel28BrokerRequestAuditRequireDryRunOnly = true
InpLevel28BrokerRequestAuditRequireZeroVolume = true
InpLevel28BrokerRequestAuditRequireNoSendContract = true
InpLevel28BrokerRequestAuditRequireRequestValidatorCoherence = true
InpLevel28BrokerRequestAuditRequireSafetyIntentCoherence = true
InpLevel28BrokerRequestAuditFolder = "FlagCountingPhoenix"
```

## What it audits

Level 28 audits:

```text
dry_run_only is still true
request volume is still zero
no-send contract is intact
validator did not pass without a built dry-run request
validator did not pass while dry_run_only was false
validator did not pass while volume was non-zero
validator request id matches dry-run request id
built request did not bypass safety gate
built request did not bypass allowed paper intent
```

## Audit statuses

```text
BROKER_REQUEST_AUDIT_PASSED_NO_SEND
BROKER_REQUEST_AUDIT_BLOCKED
BROKER_REQUEST_AUDIT_DUPLICATE_SKIPPED
```

## Audit block reasons

```text
BLOCK_AUDIT_DRY_RUN_ONLY_FALSE
BLOCK_AUDIT_VOLUME_NOT_ZERO
BLOCK_AUDIT_NO_SEND_CONTRACT_BROKEN
BLOCK_AUDIT_REQUEST_VALIDATOR_INCOHERENT
BLOCK_AUDIT_SAFETY_INTENT_INCOHERENT
```

## Request chain states

```text
REQUEST_CHAIN_BUILT_AND_VALIDATED_NO_SEND
REQUEST_CHAIN_BUILT_BUT_VALIDATOR_BLOCKED
REQUEST_CHAIN_NOT_BUILT
REQUEST_CHAIN_UNKNOWN
```

## Duplicate handling

The EA can recalculate the same audit state repeatedly.

Level 28 builds a dedupe key from:

```text
request_key
validator_status
audit block reason
request chain state
```

If the same audit key repeats and duplicate skipping is enabled, the audit ledger does not append the same row again.

## No-send contract

Every output row explicitly includes:

```text
AUDIT_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE
```

and:

```text
REAL_EXECUTION_DISABLED_LEVEL28_BROKER_REQUEST_AUDIT_ONLY
```

## Relationship to previous layers

Level 20 answers:

```text
Do we have entry / invalidation / destination anchors?
```

Level 21 answers:

```text
Can those anchors seed a paper intent?
```

Level 22 answers:

```text
What would the close-only lifecycle state be?
```

Level 23 answers:

```text
What is the performance-style summary?
```

Level 24 answers:

```text
Is the stack safe enough for a future dry-run broker layer?
```

Level 25 answers:

```text
What would the broker-like request preview look like?
```

Level 26 answers:

```text
Is that preview compatible with basic symbol/broker constraints without sending anything?
```

Level 27 answers:

```text
What is the historical ledger of request previews and validator outcomes?
```

Level 28 answers:

```text
Is the entire no-send request chain internally coherent?
```

## Next correct layer

The next layer should be:

```text
Level 29 — Paper Broker Adapter / Still No Send
```

Level 29 can start converting the validated no-send request chain into a pure internal paper-broker state machine, still without calling `OrderSend`, `OrderCheck`, or `CTrade`.
