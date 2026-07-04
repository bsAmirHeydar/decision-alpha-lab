# SCN-R03 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
scenario ranking model
convex opportunity set model
multi-zone selection policy
potential-first scenario logic
post-convexity win-rate rule
risk budget per opportunity
conditional scenario planning
scenario veto policy
```

## Core Hard Rules

```text
NO_SCENARIO_MUST_BECOME_DOMINANT_BY_DEFAULT
POTENTIAL_OVER_CORRECTNESS
CONVEXITY_BEFORE_WIN_RATE
EACH_SCENARIO_IS_EVALUATED_BY_ITS_OWN_EVIDENCE
MULTIPLE_SCENARIOS_CAN_REMAIN_ALIVE
MULTIPLE_ZONES_CAN_REMAIN_ALIVE
OPPOSITE_SCENARIOS_CAN_COEXIST_AS_CONDITIONAL_PLANS
```

## Core Learnable Policies

```text
convexity_score
cost_to_potential_ratio
reward_path_openness
risk_budget_per_zone
post_convexity_win_rate
scenario_family_stability
multi_zone_execution_priority
conditional_plan_activation
```

## Proposed Objects

```text
ConvexOpportunitySet
ScenarioThread
ZoneOpportunity
ConditionalScenarioPlan
RiskBudgetAllocation
ScenarioVeto
PostConvexityPerformance
```

## Proposed Datasets

```text
scenario_ranking_model_v1.csv
multi_zone_selection_policy_v1.csv
scenario_veto_policy_v1.csv
risk_budget_per_zone_v1.csv
conditional_scenario_plan_v1.csv
convex_opportunity_set_v1.csv
post_convexity_winrate_model_v1.csv
scenario_thread_outcome_ledger_v1.csv
```

## Proposed Fields

```text
opportunity_set_id
scenario_thread_id
scenario_id
zone_id
direction
symbol
timeframe
scale_id

evidence_set
constraint_set
zone_family
entry_family
destination_set

entry_cost
stop_distance
risk_distance
reward_distance
reward_path_openness
destination_openness
optionality_score
explosion_potential_score
convexity_score
cost_to_potential_ratio

scenario_state
scenario_priority
is_primary_opportunity
is_secondary_opportunity
is_watchlist
is_conditional_plan
is_vetoed

post_convexity_win_rate
sample_size
scenario_family_stability
tested_expectancy_after_convexity

risk_budget
risk_budget_reason
entry_permission_state
activation_condition
veto_reason
last_rank_update_reason
```

## Proposed Labels

```text
CONVEX_OPPORTUNITY_SET
SCENARIO_THREAD
POTENTIAL_OVER_CORRECTNESS
CONVEXITY_BEFORE_WIN_RATE
PRIMARY_CONVEX_OPPORTUNITY
SECONDARY_CONVEX_OPPORTUNITY
WATCHLIST_CONVEX_OPPORTUNITY
CONDITIONAL_LONG_PLAN
CONDITIONAL_SHORT_PLAN
VETOED_NON_CONVEX

LOW_COST_HIGH_REWARD
OPEN_REWARD_PATH
WIDE_PROFIT_POTENTIAL
POST_CONVEXITY_WIN_RATE
```

## Proposed AI Modules

```text
Convex Opportunity Set Builder
Scenario Thread Builder
Scenario Convexity Scorer
Cost-to-Potential Ranker
Reward Path Openness Scorer
Multi-Zone Selection Policy
Risk Budget Allocator
Conditional Plan Router
Scenario Veto Model
Post-Convexity Win Rate Evaluator
Scenario Rank Update Engine
```

## Architecture Consequence

The scenario layer should not produce one forced direction.

It should produce a set:

```text
ConvexOpportunitySet
```

The execution layer should then activate only the opportunity whose zone is reached and whose lower-timeframe entry refinement becomes valid.

This keeps NDS aligned with optionality rather than prediction.

## Open Questions

1. What minimum convexity score is required before win rate is considered?
2. How should cost-to-potential ratio be calculated?
3. Should convexity be measured in R-multiple potential, destination distance, or distribution tail size?
4. What exact conditions activate a conditional scenario plan?
5. Can two opposite conditional plans be active at the same price area?
6. How should total risk be capped across multiple live opportunities?
7. Should unused risk from a missed zone transfer to another zone?
8. What is the maximum number of live scenario threads allowed?
9. How often should scenario ranks update?
10. What sample size is required for post-convexity win rate to matter?
11. Should low win-rate but high-tail scenarios remain alive indefinitely?
12. How should overlapping zones be handled inside the opportunity set?
13. Should scenario family performance be tracked globally, per market, per timeframe, and dynamically?
14. What exact state turns a watchlist opportunity into an executable opportunity?
15. Should the first implementation be a deterministic ranking table before AI ranking?

## Attachment Index

No images were provided for this answer.
