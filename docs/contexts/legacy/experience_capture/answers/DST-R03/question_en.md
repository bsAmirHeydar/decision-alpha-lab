# DST-R03 — Destination Repricing and Completion

## Question

How should Destination candidates update, reprice, complete, become consumed, or lose usefulness as market structure evolves?

## Why This Question Remains

DST-R01 established that destination logic is trainable and can emerge from later F-counting, open one-and-two structures, and counting inside the higher Hook. DST-R02 established that exits should preserve profit openness and should prefer trained partial-close logic over default trailing.

DST-R03 defines the boundary of destination lifecycle: whether destination repricing and completion should use only NDS anatomy and internal weights, or whether any external target logic is allowed.

## Answer Requirements

Please clarify:

- Should destination lifecycle use only NDS anatomy?
- Should destination weighting use the same weights and logic already used elsewhere in the system?
- Is there any extra external destination logic?
- How should repricing happen when new NDS structure forms?
- How should completion or consumption be judged?
- Should destination candidates remain historical after they lose usefulness?
- Should opposite destination candidates be evaluated through the same anatomy?
- What should the final output model contain?

## Expected Output

```text
destination_state_machine_v1
destination_repricing_policy_v1
destination_completion_policy_v1
destination_consumption_model_v1
nds_only_destination_lifecycle_v1
destination_weight_update_model_v1
destination_audit_ledger_v1
```
