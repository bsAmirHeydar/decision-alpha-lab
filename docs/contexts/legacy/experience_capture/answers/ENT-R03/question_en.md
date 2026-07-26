# ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

## Question

After a Limit Entry is created from a valid Entry-Level Extreme, how long should the pending limit remain alive, when should it be canceled or deleted, and how should missed or replacement behavior be defined?

## Why This Question Remains

ENT-R01 defined the Entry-Level Extreme as Extreme Near Death. ENT-R02 defined the practical entry geometry: limit entry, stop behind node, trainable buffer, spread adjustment, and max-lot splitting.

ENT-R03 defines the lifecycle of the pending limit before fill.

## Answer Requirements

Please clarify:

- While the parent zone is alive but price has not reached the limit, how long does the pending order remain alive?
- If the scenario, zone, or original reason that created the order becomes invalid, should the pending order be canceled immediately?
- If the entry-scale node or death boundary is hit before fill, what happens?
- If price moves without filling the order, is it missed or should the system seek replacement?
- What does "missed" mean?
- When is replacement allowed?
- Does the new entry need to be better than the previous one?
- If a previous order is still alive and a new Entry-Level Extreme appears, should both remain or should the old one be canceled?
- Should a pending order have time expiration or only structural expiration?
- What states should the final state machine contain?

## Expected Output

```text
pending_limit_state_machine_v1
cancel_policy_v1
missed_entry_policy_v1
replace_entry_policy_v1
pending_order_structural_expiration_v1
reason_integrity_pending_order_model_v1
```
