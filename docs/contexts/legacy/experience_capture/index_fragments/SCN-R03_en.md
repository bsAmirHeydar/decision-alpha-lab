# Index Fragment — SCN-R03

## SCN-R03 — Scenario Ranking and Multi-Zone Selection

Path:

```text
docs/contexts/legacy/experience_capture/answers/SCN-R03/
```

Summary:

In NDS, multiple scenarios do not need to collapse into one dominant truth. Each scenario is evaluated by its own NDS evidence and by whether it offers a convex trade: lower cost, larger possible reward, wider reward path, and more open optionality. Potential matters more than correctness. Every scenario should be continuously tested, but ranking should first prioritize convexity and cost-to-potential quality. Win rate matters only after convexity has been established. The system should output a live Convex Opportunity Set containing primary, secondary, watchlist, conditional, and vetoed scenario threads.

Main derived architecture requirements:

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
