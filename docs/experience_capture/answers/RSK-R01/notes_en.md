# RSK-R01 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
hierarchical risk budget model
context risk cost model
zone risk cost model
entry risk cost model
aggregate risk tolerance model
risk reward scoring model
trainable risk allocation policy
```

## Core Hard Rules

```text
RISK_MUST_BE_MEASURED_AT_CONTEXT_ZONE_AND_ENTRY_LEVELS
CONTEXTS_CAN_BE_EXPENSIVE_OR_CLEAN
ZONES_CAN_BE_EXPENSIVE_OR_CLEAN
ENTRIES_CAN_BE_EXPENSIVE_OR_CLEAN
RISK_BUDGET_MUST_BE_TRAINED
RISK_MUST_BE_EVALUATED_AGAINST_PROFIT_AND_REWARD
AGGREGATE_RISK_TOLERANCE_MUST_BE_MEASURED
RISK_SCORING_IS_REQUIRED
```

## Core Learnable Policies

```text
context_risk_cost_score
zone_risk_cost_score
entry_risk_cost_score
context_cleanliness_score
zone_cleanliness_score
entry_cleanliness_score
aggregate_risk_tolerance
risk_to_reward_quality
risk_budget_permission
risk_reduction_policy
risk_veto_threshold
```

## Proposed Objects

```text
ContextRiskProfile
ZoneRiskProfile
EntryRiskProfile
AggregateRiskTolerance
RiskBudgetScore
RiskRewardProfile
RiskAllocationDecision
RiskVeto
OpportunityRiskLedger
```

## Proposed Datasets

```text
risk_budget_per_opportunity_set_v1.csv
risk_allocation_policy_v1.csv
context_risk_cost_model_v1.csv
zone_risk_cost_model_v1.csv
entry_risk_cost_model_v1.csv
risk_reward_tolerance_model_v1.csv
risk_score_model_v1.csv
aggregate_risk_profile_v1.csv
risk_veto_policy_v1.csv
risk_family_performance_v1.csv
```

## Proposed Fields

```text
opportunity_set_id
scenario_id
zone_id
entry_extreme_id
position_id
symbol
timeframe
scale_id
direction

context_id
zone_family_id
entry_family_id
reason_set_id

context_risk_cost_score
context_cleanliness_score
context_decision_expense
context_reward_compensation
context_post_convexity_win_rate
context_tail_capture

zone_risk_cost_score
zone_cleanliness_score
zone_width
zone_invalidation_distance
zone_reward_openness
zone_cost_to_potential
zone_failure_rate

entry_risk_cost_score
entry_cleanliness_score
entry_stop_distance
entry_buffer_cost
spread_cost
fill_probability
near_death_quality
cost_compression_score

aggregate_risk_cost_score
aggregate_risk_tolerance
aggregate_risk_spent
aggregate_reward_expected
aggregate_reward_realized
reward_openness_score
tail_potential_score
convexity_score

risk_budget_permission
risk_budget_score
risk_reduction_required
risk_vetoed
risk_veto_reason
trained_policy_id
sample_size
confidence_score
```

## Proposed Labels

```text
CONTEXT_EXPENSIVE
CONTEXT_CLEAN_LOW_COST
ZONE_EXPENSIVE
ZONE_CLEAN_LOW_COST
ENTRY_EXPENSIVE
ENTRY_CLEAN_LOW_COST
AGGREGATE_RISK_ACCEPTABLE
AGGREGATE_RISK_TOO_HIGH
REWARD_COMPENSATES_RISK
REWARD_DOES_NOT_COMPENSATE_RISK
RISK_BUDGET_APPROVED
RISK_BUDGET_REDUCED
RISK_BUDGET_VETOED
```

## Proposed AI Modules

```text
Context Risk Cost Learner
Zone Risk Cost Learner
Entry Risk Cost Learner
Aggregate Risk Tolerance Model
Risk-to-Reward Scorer
Risk Budget Allocator
Risk Veto Router
Risk Family Performance Evaluator
Opportunity Risk Ledger Builder
```

## Architecture Consequence

Risk cannot be a flat number attached only at execution time.

Recommended flow:

```text
ContextRiskProfile
→ ZoneRiskProfile
→ EntryRiskProfile
→ AggregateRiskTolerance
→ RiskRewardScore
→ RiskBudgetDecision
```

This should happen before any ExecutionIntent is considered for validation.

## Open Questions

1. What exact metrics define an expensive context?
2. What exact metrics define a clean context?
3. What exact metrics define an expensive zone?
4. What exact metrics define a clean zone?
5. What exact metrics define an expensive entry?
6. What exact metrics define a clean entry?
7. Should context risk dominate zone and entry risk?
8. Can a very clean entry compensate for an expensive context?
9. Can a very strong context compensate for an expensive entry?
10. Should risk scores be normalized per symbol/timeframe?
11. What sample size is required before risk scores can be trusted?
12. Should risk allocation be deterministic first and trained later?
13. Should risk be reduced gradually or vetoed sharply when cost is high?
14. How should aggregate risk across multiple live opportunities be capped?
15. How should this risk model connect to RSK-R02 convexity metrics?

## Attachment Index

No images were provided for this answer.
