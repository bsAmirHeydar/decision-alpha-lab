# ENT-R02 — Normalized Interpretation

## Core Claim

Entry execution after an Entry-Level Extreme is limit-based.

The canonical entry method is:

```text
LIMIT_ENTRY
```

The stop belongs behind the relevant node.

The exact extra room behind the node is not a hard constant. It is a trainable buffer policy.

The system must also apply spread adjustment rules and split orders if the required volume exceeds maximum allowed lot.

## Stop Geometry

The stop is placed behind the node.

Hard rule:

```text
stop_reference = relevant entry node
stop_location = behind node
```

This follows the NDS principle that invalidation must be structural.

The node is the structural death boundary or protection boundary for the entry.

## Trainable Buffer Behind Node

Although the stop is behind the node, the exact extra room can matter.

The user states that sometimes giving the stop a few points of room improves the result.

Therefore:

```text
stop_buffer_points = trainable
```

This buffer should not be interpreted as discretionary leniency.

It is a tested execution-geometry parameter.

Possible forms:

```text
fixed points
spread multiple
symbol tick multiple
market-specific buffer
timeframe-specific buffer
zone-family-specific buffer
dynamic trained buffer
```

The first implementation can log all candidates and later train/test buffer variants.

## Limit Entry

Entry is limit.

Hard rule:

```text
entry_order_type = LIMIT
```

This supports the wider NDS principle:

```text
We do not trade confirmation.
We do not chase.
We use low-cost predefined entry geometry.
```

## Spread Adjustment Rules

The user defines explicit spread adjustment rules.

### Buy Limit

For a buy limit:

```text
buy_limit_entry_price = desired_entry_price + spread
```

Interpretation:

The intended structural buy level is adjusted upward by spread so that practical execution reflects the real fill side.

### Sell Limit

For a sell limit:

```text
sell_limit_stop_loss = structural_stop_loss + spread
sell_limit_take_profit = structural_take_profit + spread
```

Interpretation:

For sell limit trades, both stop loss and take profit are shifted upward by spread.

This rule should be implemented in the execution-intent or broker-validation layer, while remaining explicitly recorded as part of the practical policy.

## Broker Constraints

Broker constraints should not redefine NDS ontology.

They should be handled by the execution validator.

Examples:

```text
minimum stop distance
tick size
lot step
maximum lot
minimum lot
freeze level
spread
symbol digits
```

If broker constraints make the intended geometry impossible, the execution layer should not silently distort the NDS idea.

It should either:

```text
adjust according to allowed explicit policy
or veto the execution intent
```

## Max Lot Split Policy

If the desired position size exceeds the broker's maximum lot per order, split the order into multiple trades.

Rule:

```text
if requested_volume > max_lot:
    split into multiple orders
```

Suggested fields:

```text
requested_volume
max_lot
order_count
split_volumes
remaining_volume
```

This belongs to practical execution handling, not NDS signal logic.

## ExecutionIntent Contract

ENT-R02 should output an execution intent, not directly send orders.

The execution intent should contain all practical fields required for downstream validation:

```text
order_type
direction
entry_price
stop_loss
take_profit
spread_adjustment_applied
stop_buffer_points
risk_budget
volume_requested
split_required
split_orders
cancel_conditions
replace_conditions
veto_reason
```

This aligns with the broader architecture rule:

```text
AI / NDS produces ExecutionIntent.
Safety Gate / Validator / Broker layer decides final sendability.
```

## Limit Fill, Missed, and Replace Policy

The user did not fully define missed/replace behavior in this answer.

Therefore, this section remains policy-learning territory.

Initial interpretation:

```text
limit entry is preferred
missed limit should be logged
replace behavior should depend on whether a new Entry-Level Extreme appears inside the same valid zone
cancel should occur if the node/death boundary, parent zone, or parent scenario becomes invalid
```

## Machine-Readable Summary

```text
entry_method = LIMIT
stop = behind relevant node
stop_buffer = trainable
buy_limit_entry = desired_entry + spread
sell_limit_sl = structural_sl + spread
sell_limit_tp = structural_tp + spread
if max_lot is exceeded, split order into several trades
broker constraints are execution-validator concerns
```

## Short Formal Statement

ENT-R02 defines the practical entry geometry after an Entry-Level Extreme. Entry is limit-based. The stop goes behind the relevant node. A small extra buffer behind the node may improve results and must be trained rather than guessed. Buy limit entry price is adjusted upward by spread. For sell limit trades, stop loss and take profit are adjusted upward by spread. If requested volume exceeds max lot, the order must be split into multiple trades. These rules should produce an ExecutionIntent for validation, not direct order sending.
