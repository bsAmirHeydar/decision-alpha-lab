# Flag Counting Level 25 — Broker Dry Run Only

## Purpose

Level 25 adds a broker-like request preview after the Level 24 Safety Gate.

This is still not execution.

It does not call `OrderSend`.

It does not use `CTrade`.

It does not create a broker request.

It does not create a position.

It does not calculate volume or account risk.

The goal is to see what a future broker request would look like if the safety gate and paper intent allow it.

## Hard boundary

Level 25 does not modify:

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
dry-run only
no OrderSend
no CTrade
no OrderCheck
no position
no volume sizing
no risk sizing
no real execution
```

## New output

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level25_broker_dry_run.csv
```

## New inputs

```text
InpLevel25BrokerDryRunEnabled = true
InpLevel25BrokerDryRunExportCsv = true
InpLevel25BrokerDryRunPrintSummary = false
InpLevel25BrokerDryRunRequireSafetyGatePassed = true
InpLevel25BrokerDryRunRequireIntentAllowed = true
InpLevel25BrokerDryRunOnly = true
InpLevel25BrokerDryRunMagic = 250025
InpLevel25BrokerDryRunComment = "DAL_L25_DRY_RUN_ONLY"
InpLevel25BrokerDryRunFolder = "FlagCountingPhoenix"
```

## Request preview fields

The dry-run row includes:

```text
request_id
request_key
request_action
request_order_type
request_direction
request_volume
request_price
request_sl
request_tp
request_deviation_points
request_magic
request_comment
dry_run_only
request_built
dry_run_status
block_reason
request_validity_status
```

## Order type preview

For bullish paper intent:

```text
ORDER_TYPE_BUY_LIMIT_PREVIEW
```

For bearish paper intent:

```text
ORDER_TYPE_SELL_LIMIT_PREVIEW
```

These are strings only.

They are not MQL5 order requests.

## Volume policy

Level 25 intentionally sets:

```text
request_volume = 0.0
```

This prevents accidental interpretation as a tradable request.

Volume and risk sizing are not Level 25 responsibilities.

## Safety dependency

By default, Level 25 requires Level 24 to pass:

```text
InpLevel25BrokerDryRunRequireSafetyGatePassed = true
```

If the safety gate blocks, Level 25 outputs:

```text
BROKER_DRY_RUN_BLOCKED_SAFETY_GATE
```

## Intent dependency

By default, Level 25 requires Level 21 paper intent to be allowed:

```text
InpLevel25BrokerDryRunRequireIntentAllowed = true
```

If intent is blocked, Level 25 outputs:

```text
BROKER_DRY_RUN_BLOCKED_INTENT_NOT_ALLOWED
```

## Dry-run lock

Level 25 must remain dry-run only:

```text
InpLevel25BrokerDryRunOnly = true
```

If this is false, the dry-run itself blocks:

```text
BROKER_DRY_RUN_BLOCKED_DRY_RUN_ONLY_FALSE
```

## Statuses

```text
BROKER_DRY_RUN_REQUEST_BUILT_CSV_ONLY
BROKER_DRY_RUN_BLOCKED_DRY_RUN_ONLY_FALSE
BROKER_DRY_RUN_BLOCKED_SAFETY_GATE
BROKER_DRY_RUN_BLOCKED_INTENT_NOT_ALLOWED
BROKER_DRY_RUN_BLOCKED_NO_DIRECTION
BROKER_DRY_RUN_BLOCKED_MISSING_PRICES
BROKER_DRY_RUN_BLOCKED_PRICE_GEOMETRY
```

## Request validity statuses

```text
REQUEST_VALID_DRY_RUN_PREVIEW_ONLY
REQUEST_INVALID_DRY_RUN_FLAG
REQUEST_BLOCKED_BY_SAFETY_GATE
REQUEST_BLOCKED_BY_INTENT
REQUEST_INVALID_NO_DIRECTION
REQUEST_INVALID_MISSING_PRICES
REQUEST_INVALID_PRICE_GEOMETRY
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
What would the broker-like request preview look like, without sending anything?
```

## Next correct layer

The next layer should be:

```text
Level 26 — Broker Request Validator / No Send
```

Level 26 should still not send orders. It can validate symbol digits, stop distance, tick size alignment, and broker minimum stop distance, but it must not call `OrderSend`.
