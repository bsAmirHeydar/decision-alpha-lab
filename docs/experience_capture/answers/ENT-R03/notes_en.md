# ENT-R03 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
pending limit lifecycle policy
reason integrity model
structural expiration policy
pending order cancel/delete policy
missed entry open policy
replace entry open policy
```

## Core Hard Rules

```text
PENDING_LIMIT_LIVES_WHILE_TRADE_REASONS_REMAIN_VALID
PENDING_LIMIT_IS_DELETED_WHEN_TRADE_REASONS_FAIL
PENDING_ORDER_LIFECYCLE_IS_REASON_BASED
STRUCTURAL_EXPIRATION_IS_PRIMARY
```

## Core Learnable Policies

```text
missed_entry_definition
replace_entry_policy
reason_weakening_threshold
whether weakened reasons cancel immediately or downgrade order state
time_expiration_as_secondary_safety
better_entry_replacement_threshold
```

## Proposed Objects

```text
PendingLimitIntent
TradeReasonSet
TradeReasonIntegrity
PendingLimitState
PendingLimitCancelEvent
PendingLimitMissedEvent
PendingLimitReplaceEvent
StructuralExpiration
```

## Proposed Datasets

```text
pending_limit_state_machine_v1.csv
cancel_policy_v1.csv
missed_entry_policy_v1.csv
replace_entry_policy_v1.csv
pending_order_structural_expiration_v1.csv
reason_integrity_pending_order_model_v1.csv
pending_limit_lifecycle_ledger_v1.csv
```

## Proposed Fields

```text
pending_limit_id
execution_intent_id
scenario_id
zone_id
entry_extreme_id
reference_node_id
destination_id
reason_set_id

order_type
direction
entry_price
stop_price
take_profit
spread_adjustment_applied
stop_buffer_points

trade_reason_count
core_reason_count
intact_reason_count
weakened_reason_count
invalidated_reason_count
trade_reason_integrity_score
core_reason_broken

pending_state
previous_pending_state
state_transition_reason
created_time
last_reason_check_time
deleted_time
filled_time

is_alive
is_deleted
is_canceled
is_missed
is_replaced
is_filled
is_structurally_expired

cancel_reason
delete_reason
missed_reason
replace_reason
replacement_pending_limit_id

parent_scenario_state
parent_zone_state
entry_extreme_state
reference_node_state
convexity_state
destination_state
```

## Proposed Labels

```text
PENDING_LIMIT_CREATED
PENDING_LIMIT_ALIVE
REASON_INTEGRITY_INTACT
REASON_INTEGRITY_WEAKENED
REASON_INTEGRITY_INVALIDATED
PENDING_LIMIT_DELETED_BY_REASON_FAILURE
PENDING_LIMIT_CANCELED_BY_REASON_INVALIDATION
PENDING_LIMIT_STRUCTURALLY_EXPIRED
PENDING_LIMIT_MISSED
PENDING_LIMIT_REPLACED
PENDING_LIMIT_FILLED
```

## Proposed AI Modules

```text
Pending Limit Reason Integrity Tracker
Pending Limit State Machine
Pending Limit Cancel Router
Structural Expiration Detector
Missed Entry Classifier
Replace Entry Policy Learner
Pending Limit Lifecycle Auditor
```

## Architecture Consequence

The pending order engine should not keep orders alive only because they have not expired by time.

It should re-check the reason set.

Recommended flow:

```text
PendingLimitIntent
→ check TradeReasonSet
→ compute reason integrity
→ if reasons intact: keep alive
→ if reasons invalid: delete/cancel
→ log state transition
```

This should happen before any broker send or pending order maintenance.

## Open Questions

1. Which reasons are core reasons versus secondary reasons?
2. Does any core reason failure cancel immediately?
3. Can a pending order remain alive if reasons are weakened but not invalidated?
4. Should weakened reasons move the order to `PENDING_LIMIT_REASON_WEAKENED`?
5. Is time expiration ever allowed as a secondary safety rule?
6. What exactly defines a missed limit?
7. Can a missed order remain eligible for replacement?
8. Should replacement require a new `pending_limit_id`?
9. Can replacement occur inside the same reason set, or must it create a new reason set?
10. If a better entry appears while the old order is still valid, should the old order be canceled?
11. Does replace require improved convexity?
12. Should pending order maintenance run every tick, every bar, or on structural events only?
13. Should deleted pending orders remain in the audit ledger?
14. How should this integrate with broker-side pending orders in live mode?
15. Should the initial implementation be no-send only with audit logs?

## Attachment Index

No images were provided for this answer.
