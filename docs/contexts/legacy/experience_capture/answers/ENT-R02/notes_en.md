# ENT-R02 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
limit entry policy
stop geometry model
trainable buffer policy
spread adjustment policy
execution intent contract
max lot split policy
broker validation boundary
```

## Core Hard Rules

```text
ENTRY_IS_LIMIT
STOP_GOES_BEHIND_NODE
BUY_LIMIT_ENTRY_PRICE_ADJUSTS_UP_BY_SPREAD
SELL_LIMIT_STOP_LOSS_ADJUSTS_UP_BY_SPREAD
SELL_LIMIT_TAKE_PROFIT_ADJUSTS_UP_BY_SPREAD
MAX_LOT_REQUIRES_ORDER_SPLITTING
BROKER_CONSTRAINTS_DO_NOT_REDEFINE_NDS_ONTOLOGY
```

## Core Learnable Policies

```text
stop_buffer_points
best_buffer_by_symbol
best_buffer_by_timeframe
best_buffer_by_zone_family
missed_limit_replace_policy
cancel_after_missed_policy
entry_repricing_policy
veto_when_broker_adjustment_is_too_large
```

## Proposed Objects

```text
LimitEntryIntent
StopGeometry
EntryBufferPolicy
SpreadAdjustment
BrokerValidationRequest
MaxLotSplitPlan
ExecutionIntent
FillMissedReplaceState
```

## Proposed Datasets

```text
limit_entry_policy_v1.csv
stop_geometry_model_v1.csv
entry_buffer_policy_v1.csv
spread_adjustment_policy_v1.csv
fill_missed_replace_policy_v1.csv
execution_intent_contract_v1.csv
max_lot_split_policy_v1.csv
broker_validation_request_v1.csv
```

## Proposed Fields

```text
execution_intent_id
scenario_id
zone_id
entry_extreme_id
symbol
direction
order_type

structural_entry_price
adjusted_entry_price
entry_spread_adjusted
spread_points
spread_price_value

reference_node_id
structural_stop_price
stop_buffer_points
stop_buffer_policy_id
adjusted_stop_loss
stop_behind_node_valid

structural_take_profit
adjusted_take_profit
take_profit_spread_adjusted

risk_budget
requested_volume
max_lot
min_lot
lot_step
split_required
split_order_count
split_volumes

broker_min_stop_distance_ok
tick_size_ok
freeze_level_ok
execution_validator_required

cancel_if_node_invalidated
cancel_if_zone_destroyed
cancel_if_scenario_dead
replace_if_new_entry_extreme
missed_if_price_moves_without_fill

execution_permission_state
veto_reason
```

## Proposed Labels

```text
LIMIT_ENTRY
STOP_BEHIND_NODE
TRAINABLE_STOP_BUFFER
BUY_LIMIT_ENTRY_SPREAD_ADJUSTED
SELL_LIMIT_SL_SPREAD_ADJUSTED
SELL_LIMIT_TP_SPREAD_ADJUSTED
MAX_LOT_SPLIT_REQUIRED
BROKER_VALIDATION_REQUIRED
EXECUTION_INTENT_ONLY
```

## Proposed AI Modules

```text
Limit Entry Intent Builder
Stop Geometry Builder
Stop Buffer Learner
Spread Adjustment Applier
Broker Validation Adapter
Max Lot Split Planner
Fill/Missed/Replace Policy Learner
Execution Intent Validator
```

## Architecture Consequence

ENT-R02 should not directly execute trades.

It should create an `ExecutionIntent`.

Recommended flow:

```text
EntryLevelExtreme
→ LimitEntryIntent
→ SpreadAdjustment
→ StopGeometry
→ BufferPolicy
→ BrokerValidationRequest
→ MaxLotSplitPlan
→ ExecutionIntent
→ Safety Gate / Validator / Broker layer
```

This preserves the no-send architecture.

## Open Questions

1. Should the stop buffer be trained globally first or per symbol/timeframe?
2. What candidate buffer values should be tested first?
3. Should buffer be measured in points, spread multiples, or node-distance percentage?
4. Can the buffer ever move the stop so far that the trade loses convexity?
5. What is the maximum allowed buffer before entry is vetoed?
6. Should buy limit stop and take profit also have any spread adjustment, or only entry?
7. For sell limit, should entry price ever be spread-adjusted, or only stop loss and take profit as stated?
8. Should max-lot split orders share the same SL/TP or allow staggered targets?
9. If split orders are created, should they share one scenario ID and one entry_extreme_id?
10. Should partial fills create a position-management event?
11. Should a missed limit be replaced only inside the same zone?
12. What exact condition defines a missed limit?
13. What exact condition cancels a pending limit before fill?
14. If broker minimum stop distance makes the intended stop impossible, should intent be vetoed or adjusted?
15. Should execution validator always log the difference between structural and adjusted prices?

## Attachment Index

No images were provided for this answer.
