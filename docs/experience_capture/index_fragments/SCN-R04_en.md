# Index Fragment — SCN-R04

## SCN-R04 — Scenario Update, Death, and Repricing

Path:

```text
docs/experience_capture/answers/SCN-R04/
```

Summary:

A scenario in NDS is created because a set of structural constraints has been respected. Its update, repricing, ranking, veto, or death should be determined by how much of those constraints remain untouched and how its relative weight changes compared with new scenarios or previously existing scenarios that have updated. A scenario can lose rank without dying. Repricing happens when the core constraint identity remains valid but the tradeable expression changes. Death happens when the core constraints that created the scenario are destroyed. Veto means the scenario still exists structurally but is not worth trading.

Main derived architecture requirements:

```text
scenario_state_machine_v1.csv
scenario_repricing_policy_v1.csv
scenario_death_policy_v1.csv
scenario_watchlist_policy_v1.csv
scenario_to_position_transition_v1.csv
constraint_integrity_model_v1.csv
scenario_weight_update_model_v1.csv
scenario_state_transition_ledger_v1.csv
scenario_relative_comparison_ledger_v1.csv
```
