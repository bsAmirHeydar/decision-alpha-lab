# Index Fragment — EXE-R01

## EXE-R01 — ExecutionIntent Contract Finalization

Path:

```text
docs/contexts/legacy/experience_capture/answers/EXE-R01/
```

Summary:

In NDS, the detailed ExecutionIntent contract is not fully known yet, but its upstream logic is known. The four-state view is evaluated fractally and becomes the context, zone, and entry layers. Trade decisions are then made according to the quality of those layers. ExecutionIntent should therefore be a quality-gated NDS intent candidate produced after context, zone, and entry pass their structural quality checks, not a direct broker order and not a raw price instruction.

Main derived architecture requirements:

```text
execution_intent_contract_v1.csv
fractal_four_state_to_intent_model_v1.csv
context_zone_entry_decision_model_v1.csv
quality_based_execution_decision_v1.csv
execution_intent_unknown_fields_v1.csv
intent_creation_quality_gate_v1.csv
execution_intent_lineage_v1.csv
```
