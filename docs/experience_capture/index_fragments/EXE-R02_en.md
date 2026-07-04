# Index Fragment — EXE-R02

## EXE-R02 — Broker Validator and Send Gate

Path:

```text
docs/experience_capture/answers/EXE-R02/
```

Summary:

In NDS, broker validation and send-gate handling are mechanical execution constraints with clear deterministic rules. They do not belong to scenario, zone, entry, or AI reasoning. The broker validator should only check whether an ExecutionIntentCandidate is mechanically valid for the broker, normalize prices and volumes when safe, split or adjust only when structural meaning is preserved, and veto when broker constraints would make the intent unsafe or structurally invalid.

Main derived architecture requirements:

```text
broker_validation_model_v1.csv
send_gate_policy_v1.csv
mechanical_execution_validator_v1.csv
broker_constraint_checklist_v1.csv
order_adjust_or_veto_policy_v1.csv
execution_veto_reason_taxonomy_v1.csv
broker_validation_audit_ledger_v1.csv
```
