# Flag Counting Level 27 — Broker Request Ledger / No Send

## Purpose

Level 27 adds an append-only ledger for the broker-like request preview and validator result.

Level 25 builds the dry-run preview.

Level 26 validates the preview without sending anything.

Level 27 records the request and validation state into a historical ledger.

This is still not execution.

It does not call `OrderSend`.

It does not call `OrderCheck`.

It does not use `CTrade`.

It does not create a broker request.

It does not create a position.

It does not calculate volume or account risk.

## Hard boundary

Level 27 does not modify:

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
append-only request ledger
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
MQL5/Files/FlagCountingPhoenix/state_gate_level27_broker_request_ledger.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_level27_broker_request_ledger.csv
```

The first file is append-only.

The second file is the latest snapshot.

## New inputs

```text
InpLevel27BrokerRequestLedgerEnabled = true
InpLevel27BrokerRequestLedgerExportCsv = true
InpLevel27BrokerRequestLedgerPrintSummary = false
InpLevel27BrokerRequestLedgerAppendCsv = true
InpLevel27BrokerRequestLedgerWriteLatestCsv = true
InpLevel27BrokerRequestLedgerSkipDuplicateRequestKey = true
InpLevel27BrokerRequestLedgerFolder = "FlagCountingPhoenix"
```

## Ledger row content

Each row records:

```text
ledger id
ledger key
ledger sequence
ledger status
ledger reason
request id
request key
request built
dry-run-only state
dry-run status
dry-run block reason
validator passed
validator status
validator block reason
validator key
safety gate status
safety gate passed
safety gate block reason
intent id
intent allowed
intent status
preview order type
preview direction
preview volume
preview entry
preview SL
preview TP
magic
comment
normalization flags
tick-alignment flags
stop-distance flags
zero-volume flag
price-geometry flag
```

## Duplicate handling

The EA can recalculate the same request preview repeatedly.

Level 27 builds a dedupe key from:

```text
request_key
validator_status
validator_block_reason
```

If the same key repeats and duplicate skipping is enabled, the ledger does not append the same request again.

It marks:

```text
BROKER_REQUEST_LEDGER_DUPLICATE_SKIPPED
```

## Ledger statuses

```text
BROKER_REQUEST_LEDGER_ACCEPTED_NO_SEND
BROKER_REQUEST_LEDGER_RECORDED_BLOCKED_NO_SEND
BROKER_REQUEST_LEDGER_DUPLICATE_SKIPPED
```

## No-send contract

Every output row explicitly includes:

```text
LEDGER_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE
```

and:

```text
REAL_EXECUTION_DISABLED_LEVEL27_BROKER_REQUEST_LEDGER_ONLY
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

## Next correct layer

The next layer should be:

```text
Level 28 — Broker Request Audit / No Send
```

Level 28 can audit ledger consistency, request invariants, and readiness for a future simulation adapter, still without calling `OrderSend`, `OrderCheck`, or `CTrade`.
