# SCN-R03 — Scenario Ranking and Multi-Zone Selection

## Question

When several scenarios, contexts, or zones are alive at the same time, how should the system rank, keep, reject, or plan them together?

## Why This Question Remains

NDS allows multiple interpretations, multiple zones, multiple destinations, multiple entry points, and different risk allocations. The system needs a policy for scenario ranking without forcing one scenario to become the only dominant truth.

## Answer Requirements

Please clarify:

- If both bullish and bearish scenarios exist, should both remain alive?
- Should several zones remain on the watchlist or should only one be selected?
- What makes a scenario or zone better?
- What creates a veto?
- Can several zones be planned with different risk?
- How should risk be split across scenarios?
- What if price reaches a weaker zone before a stronger zone?
- Can conditional long and short plans coexist?
- How should ranking update as market movement changes?
- What should the final algorithmic output be?

## Expected Output

```text
scenario_ranking_model_v1
multi_zone_selection_policy_v1
scenario_veto_policy_v1
risk_budget_per_zone_v1
conditional_scenario_plan_v1
convex_opportunity_set_v1
```
