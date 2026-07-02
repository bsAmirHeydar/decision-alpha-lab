# Flag Counting Level 29 — Paper Broker Adapter / Still No Send

## Purpose

Level 29 creates an internal paper-broker adapter record from the validated and audited no-send request chain.

Level 25 builds the broker-like dry-run preview.

Level 26 validates the preview.

Level 27 records the preview and validator result into a ledger.

Level 28 audits the no-send request chain.

Level 29 converts the validated/audited chain into a paper-broker adapter state record.

This is still not execution.

It does not call `OrderSend`.

It does not call `OrderCheck`.

It does not use `CTrade`.

It does not create a broker request.

It does not create a real position.

It does not calculate volume or account risk.

## Hard boundary

Level 29 does not modify:

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
internal paper-broker adapter only
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
MQL5/Files/FlagCountingPhoenix/state_gate_level29_paper_broker_adapter.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_level29_paper_broker_adapter.csv
```

The first file is append-only.

The second file is the latest snapshot.

## New inputs

```text
InpLevel29PaperBrokerAdapterEnabled = true
InpLevel29PaperBrokerAdapterExportCsv = true
InpLevel29PaperBrokerAdapterPrintSummary = false
InpLevel29PaperBrokerAdapterAppendCsv = true
InpLevel29PaperBrokerAdapterWriteLatestCsv = true
InpLevel29PaperBrokerAdapterSkipDuplicateAdapterKey = true
InpLevel29PaperBrokerAdapterRequireAuditPassed = true
InpLevel29PaperBrokerAdapterRequireValidatorPassed = true
InpLevel29PaperBrokerAdapterRequireRequestBuilt = true
InpLevel29PaperBrokerAdapterRequireDryRunOnly = true
InpLevel29PaperBrokerAdapterRequireZeroVolume = true
InpLevel29PaperBrokerAdapterDryRunOnly = true
InpLevel29PaperBrokerAdapterFolder = "FlagCountingPhoenix"
```

## Adapter record

Each adapter row records:

```text
adapter id
adapter key
adapter sequence
adapter status
adapter block reason
virtual ticket
paper order state
paper order lifecycle hint
request id
request key
request built
dry-run-only state
dry-run status
validator passed
validator status
validator block reason
audit passed
audit status
audit block reason
preview order type
preview direction
preview volume
preview entry
preview SL
preview TP
magic
comment
zero-volume flag
dry-run-only flag
no-send contract flag
adapter-chain coherence flag
adapter runtime state
```

## Virtual ticket

Level 29 creates an internal virtual ticket:

```text
VT_<symbol>_<timeframe>_<sequence>_<request_id>
```

This is not a broker ticket.

It is not a MetaTrader order ticket.

It is only an internal CSV identifier for the future paper-broker lifecycle.

## Adapter statuses

```text
PAPER_BROKER_ADAPTER_REGISTERED_NO_SEND
PAPER_BROKER_ADAPTER_BLOCKED
PAPER_BROKER_ADAPTER_DUPLICATE_SKIPPED
```

## Block reasons

```text
BLOCK_ADAPTER_DRY_RUN_ONLY_FALSE
BLOCK_ADAPTER_AUDIT_NOT_PASSED
BLOCK_ADAPTER_VALIDATOR_NOT_PASSED
BLOCK_ADAPTER_REQUEST_NOT_BUILT
BLOCK_ADAPTER_DRY_RUN_ONLY_BROKEN
BLOCK_ADAPTER_VOLUME_NOT_ZERO
BLOCK_ADAPTER_NO_SEND_CONTRACT_BROKEN
BLOCK_ADAPTER_CHAIN_INCOHERENT
```

## Paper order states

```text
PAPER_ORDER_STATE_REGISTERED_PENDING_PREVIEW
PAPER_ORDER_STATE_BLOCKED
PAPER_ORDER_STATE_NONE
```

## Duplicate handling

The EA can recalculate the same adapter state repeatedly.

Level 29 builds a dedupe key from:

```text
request_key
validator_status
audit_status
adapter block reason
```

If the same adapter state repeats and duplicate skipping is enabled, the adapter ledger does not append the same row again.

## No-send contract

Every output row explicitly includes:

```text
PAPER_BROKER_ADAPTER_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE
```

and:

```text
REAL_EXECUTION_DISABLED_LEVEL29_PAPER_BROKER_ADAPTER_ONLY
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

Level 29 answers:

```text
Can the coherent no-send request chain be registered as an internal paper-broker adapter record?
```

## Next correct layer

The next layer should be:

```text
Level 30 — Paper Broker Lifecycle / Still No Send
```

Level 30 can track the internal virtual ticket through pending, active, closed, expired, cancelled, or blocked paper-broker states, still without calling `OrderSend`, `OrderCheck`, or `CTrade`.
