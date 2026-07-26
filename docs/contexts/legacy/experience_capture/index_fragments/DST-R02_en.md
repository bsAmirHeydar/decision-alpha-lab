# Index Fragment — DST-R02

## DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy

Path:

```text
docs/contexts/legacy/experience_capture/answers/DST-R02/
```

Summary:

In NDS, exit policy should be trained across different variants using the same core criteria as opportunity selection: potential, keeping profits open, and low cost. Trailing stop should not be the default because prior results have not been satisfactory. The preferred direction is to close part of the profit under different NDS-defined conditions while keeping some exposure open for larger profit potential. The system should compare exit families by how well they preserve open profit, capture tail opportunities, reduce unnecessary giveback, and avoid premature full exits.

Main derived architecture requirements:

```text
take_profit_policy_v1.csv
partial_exit_policy_v1.csv
multi_destination_exit_model_v1.csv
runner_tail_position_policy_v1.csv
trailing_stop_policy_v1.csv
exit_policy_training_model_v1.csv
profit_openness_preservation_model_v1.csv
exit_policy_cost_model_v1.csv
exit_family_comparison_report_v1.csv
```
