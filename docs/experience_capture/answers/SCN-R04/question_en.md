# SCN-R04 — Scenario Update, Death, and Repricing

## Question

When market movement changes, when should a scenario remain alive, be updated, be repriced, move to watchlist, be vetoed, or die?

## Why This Question Remains

NDS allows multiple live scenarios and zones. Ranking is dynamic. A scenario is not necessarily a truth claim; it is a convex opportunity thread based on constraints. The system needs a state model for scenario updates.

## Answer Requirements

Please clarify:

- What keeps a scenario alive?
- What changes scenario rank?
- When is a scenario repriced instead of killed?
- What kills a scenario?
- What is the difference between veto and death?
- When does a scenario move to watchlist?
- What happens if price moves without entry?
- What happens after entry?
- How do destinations affect scenario continuation?
- What scenario states should exist?

## Expected Output

```text
scenario_state_machine_v1
scenario_repricing_policy_v1
scenario_death_policy_v1
scenario_watchlist_policy_v1
scenario_to_position_transition_v1
constraint_integrity_model_v1
scenario_weight_update_model_v1
```
