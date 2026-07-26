# RSK-R02 — Convexity Metrics and Cost-to-Potential Formula

## Question

How should cost, potential, optionality, reward openness, and convexity be measured so that risk can be allocated only after the opportunity is sufficiently convex?

## Why This Question Remains

Previous records established that win rate matters after convexity, not before it. RSK-R01 defined risk budgeting as a hierarchical trainable model across context, zone, and entry levels. RSK-R02 formalizes the cost-to-potential formula, the role of account-risk percentage, setup-quality coefficients, true monetary cost, target rewards above 10R, and optionality at each structural level.

## Answer Requirements

Please clarify:

- What exactly is cost?
- Is risk expressed as percent of account?
- How does setup quality affect risk percentage?
- How should stop distance and commission be included?
- Should sizing be adjusted so true cost equals target risk?
- What reward range is desired?
- Is optionality only an entry-level property?
- How should optionality be measured at context, zone, and entry levels?
- Should the formula be fixed or trainable?
- What should the final output model contain?

## Expected Output

```text
convexity_metric_model_v1
cost_to_potential_score_v1
optionality_score_v1
context_optionality_model_v1
zone_optionality_model_v1
entry_optionality_model_v1
setup_quality_risk_coefficient_v1
true_cost_position_sizing_model_v1
high_reward_target_model_v1
```
