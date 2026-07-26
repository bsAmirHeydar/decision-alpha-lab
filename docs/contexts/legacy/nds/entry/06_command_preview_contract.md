---
title: NDS Command Preview Contract
status: implemented_no_send
version: 1.0.0
---
# NDS Command Preview Contract

## 1. Definition

The Command Preview is a broker-neutral envelope showing what a future instruction would contain. It is not an `MqlTradeRequest` and does not call any trading API.

Fields:

```text
command_id
source_plan_id
command_action
order_type_preview
symbol
trade_direction
volume
price
SL
TP
expiry_bars
magic
comment
send_allowed
execution_status
```

## 2. No-send invariants

The implementation enforces:

```text
command_preview_only = true
volume = 0
send_allowed = false
execution_status = NO_SEND_NDS_COMMAND_PREVIEW_ONLY
```

The module contains no order-sending class, function, request object, or position operation.

## 3. Preview order models

The enum contains the candidate policies raised by the questionnaire:

```text
LIMIT_FIRST_EDGE
LIMIT_MID_ZONE
LIMIT_NEAR_DEATH
MARKET_AFTER_CONFIRMATION
LADDER_LIMIT
```

These names are schema preparation, not Canon approval. Default is `UNRESOLVED`, which blocks the Setup.

## 4. Future adapter boundary

When execution is eventually authorized, use a new adapter:

```text
NDSTradePlan
→ NDSExecutionAuthorization
→ BrokerRequestBuilder
→ BrokerValidator
→ RiskSizer
→ OrderCheck
→ OrderSend
→ Transaction Reconciliation
```

The future adapter must not be added directly to `FP_NDSEntryEngine.mqh`.

## 5. Idempotency requirement

A future command system needs deterministic deduplication:

```text
command_fingerprint = hash(
  symbol,
  timeframe,
  setup_id,
  plan_revision,
  order_model,
  entry,
  stop,
  target,
  expiry
)
```

The same fingerprint must not create multiple requests unless an explicit replace/amend policy exists.
