# ENT-R04 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
scenario-to-position transition
position thread model
duplicate reason trade block
position reason lock
multi-exit allowance
hedge separation policy
logical position aggregation
```

## Core Hard Rules

```text
AFTER_FILL_CREATE_POSITION_THREAD
OPEN_POSITION_LOCKS_ITS_REASON_SET
NO_DUPLICATE_TRADE_WITH_SAME_REASONS_WHILE_POSITION_IS_OPEN
EXIT_CAN_OCCUR_IN_MULTIPLE_NDS_DEFINED_PLACES
HEDGE_IS_SEPARATE_ENTRY_LOGIC
OPPOSITE_SCENARIO_DOES_NOT_AUTOMATICALLY_MEAN_HEDGE
```

## Core Learnable Policies

```text
same_reason_set_similarity_threshold
overlapping_reason_set_handling
when_new_reason_set_can_add_to_existing_position
multi_exit_plan_selection
partial_exit_percentages
runner_tail_policy
position_unlock_after_completion
hedge_entry_family_policy
```

## Proposed Objects

```text
PositionThread
PositionReasonLock
LogicalPositionBucket
PositionLineage
MultiExitPlan
ExitEvent
DuplicateReasonBlock
HedgeEntryFamily
```

## Proposed Datasets

```text
scenario_to_position_transition_v1.csv
position_thread_model_v1.csv
duplicate_reason_trade_block_v1.csv
position_reason_lock_model_v1.csv
multi_exit_state_v1.csv
split_order_position_aggregation_v1.csv
hedge_separate_entry_logic_policy_v1.csv
position_lineage_ledger_v1.csv
```

## Proposed Fields

```text
position_id
logical_position_id
scenario_id
zone_id
entry_extreme_id
execution_intent_id
pending_limit_id
fill_id
reason_set_id

position_state
position_open
position_close_time
position_completion_reason

reason_lock_active
reason_lock_start_time
reason_lock_end_time
duplicate_reason_blocked
duplicate_block_reason

entry_price
filled_price
initial_stop_price
current_stop_price
destination_set_id
exit_plan_id

multi_exit_enabled
exit_count
partial_exit_count
runner_active
final_exit_done
exit_state

is_split_order_group
child_order_count
child_order_ids
aggregate_volume
aggregate_risk

hedge_allowed
hedge_reason_set_id
hedge_entry_logic_required
opposite_scenario_seen
auto_hedge_blocked
```

## Proposed Labels

```text
POSITION_THREAD_CREATED
REASON_SET_LOCKED_TO_POSITION
DUPLICATE_REASON_ENTRY_BLOCKED
SAME_REASON_TRADE_NOT_ALLOWED_WHILE_OPEN
LOGICAL_POSITION_BUCKET
MULTI_EXIT_ALLOWED
PARTIAL_EXIT_DONE
RUNNER_ACTIVE
POSITION_COMPLETED
HEDGE_REQUIRES_SEPARATE_ENTRY_LOGIC
AUTO_HEDGE_BLOCKED
```

## Proposed AI Modules

```text
Scenario-to-Position Transition Builder
Position Reason Lock Manager
Duplicate Reason Trade Blocker
Reason Set Similarity Classifier
Logical Position Aggregator
Multi-Exit Plan Selector
Position Lifecycle Auditor
Hedge Entry Logic Router
```

## Architecture Consequence

The execution system must preserve reason lineage after fill.

Recommended flow:

```text
FillEvent
→ create PositionThread
→ lock reason_set_id
→ block duplicate same-reason entries
→ attach multi-exit plan
→ manage exits through position logic
→ keep hedge as separate entry family
```

This prevents uncontrolled repeated entries from the same structural reason.

## Open Questions

1. How exactly should "same reasons" be compared?
2. Is identical `reason_set_id` enough, or should similarity between reason sets also be measured?
3. If a new entry is based on overlapping but not identical reasons, is it allowed?
4. Can the same parent scenario create multiple positions if the entry reasons differ?
5. How should max-lot split positions be aggregated in reporting?
6. Should split child orders have separate stops/targets or shared logical management?
7. What exact event unlocks the reason set?
8. Can the same reason set be reused after full exit if the zone remains alive?
9. Does partial exit unlock any part of the reason set?
10. How should position management respond if the parent scenario weakens?
11. How should position management respond if a new stronger opposite scenario appears?
12. What are the NDS exit logics and how are they prioritized?
13. Should multi-exit policy be rule-based first and trained later?
14. What exact conditions define a hedge entry family?
15. Should hedge be excluded from the first implementation and only logged as a separate future module?

## Attachment Index

No images were provided for this answer.
