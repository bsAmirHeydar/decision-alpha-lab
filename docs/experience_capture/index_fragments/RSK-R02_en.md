# Index Fragment — RSK-R02

## RSK-R02 — Convexity Metrics and Cost-to-Potential Formula

Path:

```text
docs/experience_capture/answers/RSK-R02/
```

Summary:

In NDS, risk is expressed as a percentage of account equity, adjusted by a setup-quality coefficient. The executable size must be calculated so that, after stop distance and commission, the true monetary cost equals the intended risk budget. The strategy seeks rewards above 10R, so cost must be judged against large and open reward potential. Optionality is not only an entry-level concept; it must be measured separately at context, zone, and entry levels, then combined into an aggregate optionality score. Convexity is therefore a multi-level cost-to-potential relationship, not just a small stop at the final entry.

Main derived architecture requirements:

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
