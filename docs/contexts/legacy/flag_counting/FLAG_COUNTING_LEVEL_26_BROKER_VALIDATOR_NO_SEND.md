# Flag Counting Level 26 — Broker Request Validator / No Send

## Purpose

Level 26 validates the broker-like dry-run preview created by Level 25.

This is still not execution.

It does not call `OrderSend`.

It does not call `OrderCheck`.

It does not use `CTrade`.

It does not create a broker request.

It does not create a position.

It does not calculate volume or account risk.

The goal is to validate whether the Level 25 dry-run preview is structurally compatible with basic broker constraints before any future no-send request layer.

## Hard boundary

Level 26 does not modify:

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
validator only
no OrderSend
no OrderCheck
no CTrade
no position
no volume sizing
no risk sizing
no real execution
```

## New output

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level26_broker_validator.csv
```

## New inputs

```text
InpLevel26BrokerValidatorEnabled = true
InpLevel26BrokerValidatorExportCsv = true
InpLevel26BrokerValidatorPrintSummary = false
InpLevel26BrokerValidatorRequireDryRunBuilt = true
InpLevel26BrokerValidatorRequireTickAlignment = true
InpLevel26BrokerValidatorRequireStopDistance = true
InpLevel26BrokerValidatorRequireNormalizedPrices = true
InpLevel26BrokerValidatorRequireZeroVolume = true
InpLevel26BrokerValidatorRequireDryRunOnly = true
InpLevel26BrokerValidatorFolder = "FlagCountingPhoenix"
```

## What it validates

Level 26 validates:

```text
dry-run request was built
dry_run_only is still true
volume is still zero
entry / SL / TP geometry is directionally valid
prices are normalized to symbol digits
prices are aligned to tick size
SL distance is above broker stop-level minimum
TP distance is above broker stop-level minimum
```

## Symbol properties

The validator records:

```text
SYMBOL_DIGITS
SYMBOL_POINT
SYMBOL_TRADE_TICK_SIZE
SYMBOL_TRADE_STOPS_LEVEL
```

Then it derives:

```text
min_stop_distance_price = SYMBOL_TRADE_STOPS_LEVEL * SYMBOL_POINT
```

## Validation statuses

```text
BROKER_VALIDATOR_PASSED_NO_SEND
BROKER_VALIDATOR_BLOCKED
```

## Block reasons

```text
BLOCK_DRY_RUN_ONLY_FALSE
BLOCK_DRY_RUN_REQUEST_NOT_BUILT
BLOCK_VOLUME_NOT_ZERO
BLOCK_PRICE_GEOMETRY
BLOCK_PRICE_NOT_NORMALIZED
BLOCK_SL_NOT_NORMALIZED
BLOCK_TP_NOT_NORMALIZED
BLOCK_PRICE_NOT_TICK_ALIGNED
BLOCK_SL_NOT_TICK_ALIGNED
BLOCK_TP_NOT_TICK_ALIGNED
BLOCK_STOP_DISTANCE_TOO_SMALL
BLOCK_TARGET_DISTANCE_TOO_SMALL
```

## No-send contract

Every output row explicitly includes:

```text
NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE
```

and:

```text
REAL_EXECUTION_DISABLED_LEVEL26_BROKER_VALIDATOR_ONLY
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

## Next correct layer

The next layer should be:

```text
Level 27 — Broker Request Ledger / No Send
```

Level 27 can preserve a history of validated dry-run requests and their validation results, still without calling `OrderSend`, `OrderCheck`, or `CTrade`.
