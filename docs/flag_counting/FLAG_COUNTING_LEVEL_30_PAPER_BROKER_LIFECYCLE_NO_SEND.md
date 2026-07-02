# Flag Counting Level 30 — Paper Broker Lifecycle / Still No Send

## Purpose

Level 30 tracks the internal virtual ticket created by Level 29 through a close-only paper-broker lifecycle.

Level 29 registers a validated and audited no-send request chain as an internal paper-broker adapter record.

Level 30 starts the internal lifecycle for that adapter record.

This is still not execution.

It does not call `OrderSend`.

It does not call `OrderCheck`.

It does not use `CTrade`.

It does not create a broker request.

It does not create a real position.

It does not calculate volume or account risk.

## Hard boundary

Level 30 does not modify:

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
internal paper-broker lifecycle only
close-only lifecycle model
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
MQL5/Files/FlagCountingPhoenix/state_gate_level30_paper_broker_lifecycle.csv
MQL5/Files/FlagCountingPhoenix/latest_state_gate_level30_paper_broker_lifecycle.csv
```

The first file is append-only.

The second file is the latest snapshot.

## New inputs

```text
InpLevel30PaperBrokerLifecycleEnabled = true
InpLevel30PaperBrokerLifecycleExportCsv = true
InpLevel30PaperBrokerLifecyclePrintSummary = false
InpLevel30PaperBrokerLifecycleAppendCsv = true
InpLevel30PaperBrokerLifecycleWriteLatestCsv = true
InpLevel30PaperBrokerLifecycleSkipDuplicateLifecycleKey = true
InpLevel30PaperBrokerLifecycleRequireAdapterRegistered = true
InpLevel30PaperBrokerLifecycleRequireZeroVolume = true
InpLevel30PaperBrokerLifecycleCloseOnly = true
InpLevel30PaperBrokerLifecycleExpiryBars = 20
InpLevel30PaperBrokerLifecycleFolder = "FlagCountingPhoenix"
```

## Lifecycle states

```text
PAPER_BROKER_LIFECYCLE_BLOCKED
PAPER_BROKER_LIFECYCLE_BLOCKED_NO_BARS
PAPER_BROKER_LIFECYCLE_REGISTERED_PENDING
PAPER_BROKER_LIFECYCLE_ENTERED_BY_CLOSE
PAPER_BROKER_LIFECYCLE_HIT_TARGET_BY_CLOSE
PAPER_BROKER_LIFECYCLE_HIT_STOP_BY_CLOSE
PAPER_BROKER_LIFECYCLE_AMBIGUOUS_TARGET_AND_STOP_SAME_CLOSE
PAPER_BROKER_LIFECYCLE_EXPIRED_BEFORE_ENTRY
PAPER_BROKER_LIFECYCLE_EXPIRED_AFTER_ENTRY
PAPER_BROKER_LIFECYCLE_ACTIVE_OPEN_CLOSE_ONLY
```

## Paper order states

```text
PAPER_BROKER_STATE_NONE
PAPER_BROKER_STATE_BLOCKED
PAPER_BROKER_STATE_PENDING
PAPER_BROKER_STATE_ACTIVE
PAPER_BROKER_STATE_CLOSED_TARGET
PAPER_BROKER_STATE_CLOSED_STOP
PAPER_BROKER_STATE_CLOSED_AMBIGUOUS
PAPER_BROKER_STATE_EXPIRED
```

## Close-only model

Level 30 deliberately uses close-only lifecycle logic.

For entry:

```text
bullish: close <= request_price
bearish: close >= request_price
```

For target:

```text
bullish: close >= request_tp
bearish: close <= request_tp
```

For stop:

```text
bullish: close <= request_sl
bearish: close >= request_sl
```

This keeps the paper-broker lifecycle deterministic and conservative.

## Metrics

The lifecycle row records:

```text
virtual ticket
lifecycle sequence
adapter status
adapter registered
request id
request key
order type preview
direction preview
entry price
SL
TP
seed time
entry time
exit time
seed index
entry index
exit index
expiry bars
bars to entry
bars in trade
bars elapsed total
entry close
exit close
best close
worst close
MFE close distance
MAE close distance
risk distance
reward distance
realized R-like
entry condition
exit condition
paper order event
```

## Duplicate handling

The EA can recalculate the same lifecycle state repeatedly.

Level 30 builds a dedupe key from:

```text
virtual ticket
lifecycle status
entry time
exit time
realized R-like
```

If the same lifecycle state repeats and duplicate skipping is enabled, the lifecycle ledger does not append the same row again.

## No-send contract

Every output row explicitly includes:

```text
PAPER_BROKER_LIFECYCLE_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE
```

and:

```text
REAL_EXECUTION_DISABLED_LEVEL30_PAPER_BROKER_LIFECYCLE_ONLY
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

Level 30 answers:

```text
What is the internal close-only paper-broker lifecycle of that virtual ticket?
```

## Next correct layer

The next layer should be:

```text
Level 31 — Paper Broker Performance / Still No Send
```

Level 31 can summarize Level 30 lifecycle rows into paper-broker metrics, still without calling `OrderSend`, `OrderCheck`, or `CTrade`.
