# SCN-R04 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
scenario state machine
constraint integrity model
scenario repricing policy
scenario death policy
scenario watchlist policy
scenario relative weight update model
convex opportunity set update model
```

## Core Hard Rules

```text
SCENARIO_IS_BORN_FROM_RESPECTED_CONSTRAINTS
SCENARIO_LIFE_DEPENDS_ON_CONSTRAINT_INTEGRITY
SCENARIO_RANK_DEPENDS_ON_RELATIVE_WEIGHT
SCENARIO_CAN_LOSE_WEIGHT_WITHOUT_DYING
SCENARIO_DEATH_REQUIRES_CORE_CONSTRAINT_BREAK
VETO_IS_NOT_THE_SAME_AS_DEATH
REPRICING_REQUIRES_CORE_CONSTRAINT_IDENTITY_TO_REMAIN_VALID
```

## Core Learnable Policies

```text
constraint_integrity_score
relative_scenario_weight
repricing_threshold
watchlist_threshold
veto_threshold
scenario_weight_decay
scenario_weight_boost
comparison_against_new_scenarios
comparison_against_updated_scenarios
```

## Proposed Objects

```text
ScenarioThread
ScenarioConstraintSet
ScenarioConstraintIntegrity
ScenarioWeight
ScenarioRepricingEvent
ScenarioStateTransition
ScenarioVetoReason
ScenarioDeathReason
```

## Proposed Datasets

```text
scenario_state_machine_v1.csv
scenario_repricing_policy_v1.csv
scenario_death_policy_v1.csv
scenario_watchlist_policy_v1.csv
scenario_to_position_transition_v1.csv
constraint_integrity_model_v1.csv
scenario_weight_update_model_v1.csv
scenario_state_transition_ledger_v1.csv
scenario_relative_comparison_ledger_v1.csv
```

## Proposed Fields

```text
scenario_id
scenario_thread_id
opportunity_set_id
symbol
timeframe
scale_id
direction

constraint_set_id
constraint_count
intact_constraint_count
weakened_constraint_count
invalidated_constraint_count
constraint_integrity_score
core_constraint_broken

current_state
previous_state
state_transition_reason
last_update_time
last_update_bar_time

relative_scenario_weight
previous_scenario_weight
weight_delta
weight_update_reason
comparison_group_id
compared_against_new_scenarios
compared_against_updated_scenarios

zone_id
zone_state
entry_cost
reward_potential
convexity_score
optionality_score
cost_to_potential_ratio

repriced
repricing_reason
old_zone_low
old_zone_high
new_zone_low
new_zone_high
old_entry_price
new_entry_price
old_stop_price
new_stop_price

vetoed
veto_reason
dead
death_reason
archived
```

## Proposed Labels

```text
SCENARIO_BORN_FROM_CONSTRAINTS
CONSTRAINT_INTEGRITY_INTACT
CONSTRAINT_INTEGRITY_WEAKENED
CONSTRAINT_INTEGRITY_BROKEN
SCENARIO_WEIGHT_INCREASED
SCENARIO_WEIGHT_DECREASED
SCENARIO_REPRICED
SCENARIO_UPDATED
SCENARIO_WATCHLIST
SCENARIO_VETOED_BUT_ALIVE
SCENARIO_DEAD_BY_CONSTRAINT_BREAK
SCENARIO_ARCHIVED
```

## Proposed AI Modules

```text
Scenario Constraint Integrity Tracker
Scenario Relative Weight Updater
Scenario Repricing Engine
Scenario State Machine
Scenario Death Detector
Scenario Watchlist Router
Scenario Veto Router
Convex Opportunity Set Re-Ranker
Scenario State Transition Auditor
```

## Architecture Consequence

The scenario engine should not recompute scenarios as anonymous fresh objects every time.

It should preserve scenario identity and update its state.

Recommended update flow:

```text
ScenarioThread
→ check constraint integrity
→ update cost/reward/optionality
→ compare against new and updated scenarios
→ update weight
→ transition state
```

This creates an auditable scenario lifecycle.

## Open Questions

1. Which constraints are core constraints versus secondary constraints?
2. What minimum constraint integrity score keeps a scenario alive?
3. How should partial constraint weakening be measured?
4. What exact condition triggers repricing?
5. Can a repriced scenario remain the same scenario if its zone changes completely?
6. How should relative weight be normalized across opposite directions?
7. How should weight update interact with risk budget?
8. Can a vetoed scenario return to tradable state?
9. Can a dead scenario be reborn, or does it create a new scenario_id?
10. What state transition happens after actual trade entry?
11. Should filled scenarios continue in the scenario engine or move to position management?
12. Should destination consumption reduce weight or trigger completion?
13. How should scenario archives be used for AI training?
14. Should scenario update be deterministic first before AI scoring?
15. Should the first implementation log every state transition to an audit CSV?

## Attachment Index

No images were provided for this answer.
