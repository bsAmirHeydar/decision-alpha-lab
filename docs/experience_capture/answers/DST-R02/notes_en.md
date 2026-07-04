# DST-R02 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
take profit policy
partial exit policy
multi-destination exit logic
runner/tail position policy
trailing stop skeptical policy
exit policy training model
profit openness preservation model
```

## Core Hard Rules

```text
EXIT_POLICY_SHOULD_BE_TRAINED
EXIT_EVALUATION_USES_POTENTIAL_PROFIT_OPENNESS_AND_LOW_COST
TRAILING_STOP_IS_NOT_DEFAULT
PARTIAL_CLOSE_IS_PREFERRED_OVER_TRAILING_AS_INITIAL_DIRECTION
KEEPING_PROFIT_OPEN_IS_A_PRIMARY_EXIT_OBJECTIVE
```

## Core Learnable Policies

```text
partial_exit_conditions
partial_exit_percentages
number_of_partial_exits
runner_size
final_exit_condition
when_to_keep_profit_open
when_to_close_partial_profit
trailing_stop_experiment_family
trailing_stop_veto_threshold
exit_policy_cost_model
```

## Proposed Objects

```text
ExitPolicy
PartialExitPlan
MultiDestinationExitPlan
RunnerTailPosition
ExitCondition
ExitPolicyTrainingRun
TrailingStopExperiment
ProfitOpennessScore
ExitCostModel
```

## Proposed Datasets

```text
take_profit_policy_v1.csv
partial_exit_policy_v1.csv
multi_destination_exit_model_v1.csv
runner_tail_position_policy_v1.csv
trailing_stop_policy_v1.csv
exit_policy_training_model_v1.csv
profit_openness_preservation_model_v1.csv
exit_policy_cost_model_v1.csv
exit_family_comparison_report_v1.csv
```

## Proposed Fields

```text
exit_policy_id
position_id
scenario_id
zone_id
destination_set_id
reason_set_id

exit_family
exit_variant
partial_exit_enabled
partial_exit_count
partial_exit_conditions
partial_exit_percentages
runner_enabled
runner_percentage
tail_potential_enabled

trailing_enabled
trailing_family
trailing_distance
trailing_logic
trailing_default_allowed
trailing_test_only

profit_openness_score
tail_capture_score
exit_cost_score
giveback_after_open_profit
realized_vs_available_profit
average_R
median_R
max_R
R_skew
win_rate_after_convexity
exit_efficiency_score

first_exit_reason
final_exit_reason
position_completion_reason
```

## Proposed Labels

```text
EXIT_POLICY_TRAINABLE
PARTIAL_CLOSE_PREFERRED
TRAILING_STOP_NOT_DEFAULT
TRAILING_STOP_TEST_ONLY
PROFIT_OPENNESS_PRESERVED
TAIL_RUNNER_ACTIVE
PARTIAL_EXIT_DONE
FINAL_EXIT_DONE
EXIT_COST_LOW
EXIT_POLICY_REJECTED_BY_TEST
```

## Proposed AI Modules

```text
Exit Policy Trainer
Partial Exit Policy Learner
Multi-Destination Exit Selector
Runner/Tail Policy Learner
Trailing Stop Experiment Evaluator
Profit Openness Scorer
Exit Cost Model
Exit Family Comparison Engine
```

## Architecture Consequence

DST-R02 should not hard-code one exit rule.

Recommended flow:

```text
PositionThread
→ DestinationSet
→ ExitPolicyCandidates
→ train/evaluate by potential + profit openness + low cost
→ prefer partial close families unless trailing proves useful
→ keep runner/tail portion when potential remains open
```

Trailing should be treated as a tested optional family, not the default.

## Open Questions

1. What exact NDS conditions should trigger partial close?
2. Should partial close be based on destination, optionality decay, opposite scenario, or structure completion?
3. How many partial exits should be allowed?
4. What default partial percentages should be tested first?
5. What minimum runner size should remain open?
6. Can the runner be closed only by destination completion?
7. Should break-even be considered a trailing-like behavior or a separate policy?
8. What trailing variants should be tested as baselines?
9. What result would make trailing acceptable despite skepticism?
10. How should exit policy cost be calculated?
11. Should exit policies be trained globally or per market/timeframe?
12. Should partial exit performance be attributed to exit logic or destination quality?
13. How should realized versus available profit be measured?
14. Should a policy that has lower average R but smoother equity be accepted?
15. How should this integrate with risk budget and duplicate reason locks?

## Attachment Index

No images were provided for this answer.
