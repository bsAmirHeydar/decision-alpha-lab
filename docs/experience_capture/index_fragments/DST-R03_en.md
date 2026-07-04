# Index Fragment — DST-R03

## DST-R03 — Destination Repricing and Completion

Path:

```text
docs/experience_capture/answers/DST-R03/
```

Summary:

Destination lifecycle in NDS must be built only from the existing NDS anatomy, weights, and logic families. There is no separate external destination logic. Repricing, completion, consumption, and invalidation of destinations should occur when the underlying NDS structures, weights, or scenario/zone conditions change. Destination candidates can be updated, weighted, consumed, completed, invalidated, or archived, but all of those transitions must be explained through NDS-native anatomy rather than external target rules.

Main derived architecture requirements:

```text
destination_state_machine_v1.csv
destination_repricing_policy_v1.csv
destination_completion_policy_v1.csv
destination_consumption_model_v1.csv
nds_only_destination_lifecycle_v1.csv
destination_weight_update_model_v1.csv
destination_audit_ledger_v1.csv
opposite_destination_effect_model_v1.csv
```
