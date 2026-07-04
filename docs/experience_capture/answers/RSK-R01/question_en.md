# RSK-R01 — Risk Budget Across Convex Opportunity Set

## Question

When multiple scenarios, zones, and entries are alive inside a Convex Opportunity Set, how should risk be measured, allocated, reserved, or vetoed across context, zone, and entry levels?

## Why This Question Remains

Previous records established that NDS prioritizes potential, convexity, low cost, profit openness, and post-convexity win rate. However, risk cannot be allocated as one flat number. It must be measured across the NDS hierarchy: context, zone, and entry. The system needs to learn which contexts, zones, and entries are costly, which are clean, and what reward justifies each cost.

## Answer Requirements

Please clarify:

- Should risk be measured separately at context, zone, and entry levels?
- How should the system identify expensive versus clean contexts?
- How should the system identify expensive versus clean zones?
- How should the system identify expensive versus clean entries?
- Should risk budget be trained from outcome data?
- Should risk be compared against reward, profit potential, and openness?
- Should the system measure aggregate risk tolerated for a given reward?
- How should scoring be built from cost, reward, and risk tolerance?
- Should risk allocation depend more on convexity or post-convexity win rate?
- What should the final output model contain?

## Expected Output

```text
risk_budget_per_opportunity_set_v1
risk_allocation_policy_v1
context_risk_cost_model_v1
zone_risk_cost_model_v1
entry_risk_cost_model_v1
risk_reward_tolerance_model_v1
risk_score_model_v1
```
