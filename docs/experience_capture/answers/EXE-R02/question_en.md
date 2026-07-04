# EXE-R02 — Broker Validator and Send Gate

## Question

How should the broker validator and send gate treat broker constraints such as minimum stop distance, tick size, digits, lot step, min/max lot, margin, spread, freeze level, trade mode, market session, and order rejection?

## Why This Question Remains

NDS should not directly send orders. Previous records established that NDS produces an ExecutionIntent or ExecutionIntentCandidate, and broker/safety validation comes later. EXE-R02 defines the nature of the broker validator: whether it belongs to learned NDS logic or deterministic mechanical execution rules.

## Answer Requirements

Please clarify:

- Are broker constraints part of NDS ontology or mechanical validation?
- Are these rules clear and deterministic?
- Should the broker validator train anything about the market structure?
- Should the validator change the NDS reasoning?
- Should this layer merely approve, adjust mechanically, or veto?
- What should the final output model contain?

## Expected Output

```text
broker_validation_model_v1
send_gate_policy_v1
mechanical_execution_validator_v1
broker_constraint_checklist_v1
order_adjust_or_veto_policy_v1
execution_veto_reason_taxonomy_v1
```
