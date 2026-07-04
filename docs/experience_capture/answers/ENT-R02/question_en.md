# ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy

## Question

When a valid Entry-Level Extreme / Extreme Near Death exists inside a zone, how should limit entry, stop geometry, spread adjustment, buffer, fill policy, and order splitting be defined?

## Why This Question Remains

ENT-R01 defined the entry-level Extreme as Extreme Near Death: an entry-scale CycleHook excessively close to death, used to reduce stop size and improve convexity. ENT-R02 defines the practical limit-order geometry and execution-intent rules around that concept.

## Answer Requirements

Please clarify:

- Where is the limit entry placed?
- Where is the stop placed?
- Is there a buffer behind the stop?
- Is the buffer fixed or trainable?
- How should spread be handled for buy limit and sell limit?
- Should broker constraints be part of NDS or execution validation?
- If max lot is hit, should the order be split?
- What should the output object contain?

## Expected Output

```text
limit_entry_policy_v1
stop_geometry_model_v1
entry_buffer_policy_v1
spread_adjustment_policy_v1
fill_missed_replace_policy_v1
execution_intent_contract_v1
max_lot_split_policy_v1
```
