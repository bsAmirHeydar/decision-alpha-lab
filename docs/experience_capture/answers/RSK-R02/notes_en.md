# RSK-R02 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
convexity metric model
cost-to-potential formula
setup-quality risk coefficient
true cost position sizing model
account-risk percent model
high reward target model
multi-level optionality model
```

## Core Hard Rules

```text
RISK_IS_PERCENT_OF_ACCOUNT
RISK_HAS_SETUP_QUALITY_COEFFICIENT
TRUE_COST_MUST_INCLUDE_STOP_DISTANCE_AND_COMMISSION
POSITION_SIZE_MUST_MATCH_TRUE_COST_TO_TARGET_RISK
TARGET_REWARD_IS_ABOVE_10R
OPTIONALITY_IS_NOT_ONLY_ENTRY_LEVEL
OPTIONALITY_MUST_BE_MEASURED_AT_CONTEXT_ZONE_AND_ENTRY_LEVELS
CONVEXITY_IS_MULTI_LEVEL_COST_TO_POTENTIAL
```

## Core Learnable Policies

```text
setup_quality_risk_coefficient
context_optionality_score
zone_optionality_score
entry_optionality_score
aggregate_optionality_score
convexity_threshold
reward_above_10R_quality
cost_to_potential_formula
risk_coefficient_by_setup_family
market_timeframe_adjustment
```

## Proposed Objects

```text
SetupQualityRiskCoefficient
TargetRiskCost
TrueTradeCost
ContextOptionality
ZoneOptionality
EntryOptionality
AggregateOptionality
CostToPotentialScore
HighRewardTarget
ConvexityClass
```

## Proposed Datasets

```text
convexity_metric_model_v1.csv
cost_to_potential_score_v1.csv
optionality_score_v1.csv
context_optionality_model_v1.csv
zone_optionality_model_v1.csv
entry_optionality_model_v1.csv
setup_quality_risk_coefficient_v1.csv
true_cost_position_sizing_model_v1.csv
high_reward_target_model_v1.csv
reward_above_10r_policy_v1.csv
aggregate_optionality_model_v1.csv
```

## Proposed Fields

```text
opportunity_set_id
scenario_id
zone_id
entry_extreme_id
position_id
reason_set_id
symbol
timeframe
scale_id

account_equity
base_account_risk_percent
setup_quality_risk_coefficient
effective_account_risk_percent
target_risk_cost_money

stop_distance_points
stop_distance_money
commission_money
spread_cost_money
buffer_cost_money
estimated_slippage_money
true_trade_cost_money

volume_required_for_true_cost
volume_after_broker_constraints
true_cost_matches_target
cost_mismatch_money
cost_mismatch_percent

context_optionality_score
zone_optionality_score
entry_optionality_score
aggregate_optionality_score

destination_openness_score
reward_path_openness_score
tail_potential_score
explosion_potential_score
expected_reward_R
max_potential_reward_R
reward_above_10R_candidate

cost_to_potential_score
convexity_score
convexity_class
win_rate_allowed_to_matter
post_convexity_win_rate
risk_budget_vetoed
risk_budget_veto_reason
```

## Proposed Labels

```text
RISK_PERCENT_OF_ACCOUNT
SETUP_QUALITY_RISK_COEFFICIENT_APPLIED
TRUE_COST_MATCHED_TO_TARGET_RISK
STOP_AND_COMMISSION_COST_INCLUDED
REWARD_TARGET_ABOVE_10R
CONTEXT_OPTIONALITY_MEASURED
ZONE_OPTIONALITY_MEASURED
ENTRY_OPTIONALITY_MEASURED
AGGREGATE_OPTIONALITY_MEASURED
HIGH_CONVEXITY
EXTREME_CONVEXITY
NOT_CONVEX
```

## Proposed AI Modules

```text
Setup Quality Risk Coefficient Learner
True Cost Calculator
Cost-to-Potential Scorer
Context Optionality Model
Zone Optionality Model
Entry Optionality Model
Aggregate Optionality Model
High Reward Target Classifier
Convexity Classifier
Post-Convexity Win Rate Gate
```

## Architecture Consequence

Risk sizing and convexity evaluation must be linked.

Recommended flow:

```text
ContextOptionality
→ ZoneOptionality
→ EntryOptionality
→ AggregateOptionality
→ SetupQualityRiskCoefficient
→ TargetRiskCost
→ TrueTradeCost
→ CostToPotentialScore
→ ConvexityClass
→ allow post-convexity win rate evaluation
```

The system should not evaluate optionality only at entry.

The system should not treat the input risk percent as true risk unless stop distance and commission confirm it.

## Open Questions

1. What is the default base account risk percent?
2. What range should the setup-quality coefficient have?
3. Should the coefficient be capped by risk policy?
4. Should commission be included as round-trip or entry-side only?
5. Should spread and slippage be mandatory in the first true-cost model?
6. How should broker constraints alter the matched true cost?
7. What happens if exact matching is impossible due to lot step?
8. Is reward above 10R a hard target or a preferred class?
9. What minimum potential reward makes a setup convex?
10. How should context optionality be scored?
11. How should zone optionality be scored?
12. How should entry optionality be scored?
13. Can weak entry optionality be accepted if context and zone optionality are extreme?
14. Can extreme entry optionality compensate for weak context?
15. Should optionality models be global or per market/timeframe?
16. What distribution of R should be required before trusting the convexity score?
17. Should the first implementation be audit-only before risk is used for execution sizing?

## Attachment Index

No images were provided for this answer.
