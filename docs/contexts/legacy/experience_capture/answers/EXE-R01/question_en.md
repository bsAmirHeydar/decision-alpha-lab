# EXE-R01 — ExecutionIntent Contract Finalization

## Question

What should the ExecutionIntent contract contain, and how should NDS convert structural analysis into a safe executable intent without sending broker orders directly?

## Why This Question Remains

Previous records established that NDS should not directly send orders. It should produce a structured ExecutionIntent that is later validated by broker and safety layers. However, the exact field-level contract is not fully known yet. This question captures the current known boundary: the intent must be derived from the fractal four-state view through context, zone, and entry quality.

## Answer Requirements

Please clarify:

- What is known about the structure behind ExecutionIntent?
- Should the four-state view be read fractally?
- How does the four-state view become context, zone, and entry?
- Should decisions be made based on quality at those levels?
- Which parts of the ExecutionIntent contract are still unknown?
- What should remain trainable?
- What should the final output model contain?

## Expected Output

```text
execution_intent_contract_v1
fractal_four_state_to_intent_model_v1
context_zone_entry_decision_model_v1
quality_based_execution_decision_v1
execution_intent_unknown_fields_v1
```
