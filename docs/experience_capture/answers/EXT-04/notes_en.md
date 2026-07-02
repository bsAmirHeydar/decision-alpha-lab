# EXT-04 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
context-conditioned anchor-level policy
L-level testing requirement
win-rate versus reward tradeoff principle
adaptive L policy candidate
```

## Main Design Consequence

The project needs an explicit L-level test layer.

L2 should remain the default candidate, but not a blind permanent rule.

The system should store and compare candidate node levels by context.

## Proposed Datasets

```text
l_level_context_test_v1.csv
adaptive_l_policy_dataset_v1.csv
l_level_reward_winrate_tradeoff_v1.csv
node_level_context_performance_v1.csv
```

## Proposed Fields

```text
scenario_id
entry_family_type
context_type
direction
scale_role
parent_context_state
current_context_state
child_context_state
cycle_size_context

candidate_l_levels
selected_l_level
selected_l_reason

entry_count_by_l
fill_rate_by_l
win_rate_by_l
avg_r_by_l
median_r_by_l
right_tail_r_by_l
left_tail_r_by_l
profit_factor_by_l
drawdown_by_l
stop_hit_then_reverse_by_l
limit_missed_then_reversal_by_l
path_cleanliness_by_l
execution_difficulty_by_l
```

## Proposed Labels

```text
best_l_by_expected_r
best_l_by_win_rate
best_l_by_profit_factor
best_l_by_right_tail
best_l_by_low_drawdown
best_l_by_execution_cleanliness
l2_outperformed
l3_outperformed
adaptive_l_outperformed_fixed_l2
```

## Proposed AI Modules

```text
L-Level Context Tester
Adaptive L Policy Model
Reward-vs-Winrate Tradeoff Analyzer
L-Level Robustness Model
Entry Frequency vs Quality Optimizer
Scale-Role Anchor Selector
```

## Open Questions

1. Should L-level choice be tested separately for Hook and Rally contexts?
2. Should L-level choice be tested separately for bullish and bearish scenarios?
3. Should L-level choice depend on parent-scale direction?
4. Should L2 remain the default on lower-timeframe entry refinement even if higher L wins in some contexts?
5. Should the model allow layered entries across L2 and L3?
6. What matters more for Extreme: expected R, right-tail R, win rate, or path cleanliness?
7. What minimum win rate is acceptable if reward is very large?
8. What minimum reward is acceptable if win rate is high?
9. Should stop-hit-then-reverse be treated as a failure of L level or a failure of stop buffer?
10. Should missed-limit reversals push the system toward lower L or wider extreme zones?
11. Should adaptive L be rule-based before machine learning?
12. Should L-level performance be symbol-specific or universal inside NDS?
13. Should L-level performance be scale-specific?
14. How should spread affect L-level selection?
15. What is the first baseline test: fixed L2 vs fixed L3, or fixed L2 vs adaptive L?

## Attachment Index

No images were provided for this answer.
