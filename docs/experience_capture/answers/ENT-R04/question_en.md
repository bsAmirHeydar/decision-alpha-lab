# ENT-R04 — After Fill: Scenario-to-Position Transition

## Question

After a Limit Entry is filled, how should the system transition from Scenario / ExecutionIntent into an active Position? Should the scenario remain alive, should it become a PositionThread, how should duplicate entries be prevented, and how should exits or hedges be treated?

## Why This Question Remains

ENT-R01 defined Entry-Level Extreme as Extreme Near Death.  
ENT-R02 defined limit entry, stop geometry, spread adjustment, trainable buffer, and max-lot splitting.  
ENT-R03 defined pending limit lifecycle as reason-integrity based.

ENT-R04 defines what happens after fill.

## Answer Requirements

Please clarify:

- After fill, does the ScenarioThread remain alive or become a PositionThread?
- Should the system prevent duplicate trades with the same reasons while the position is open?
- If the parent scenario weakens after entry, what happens to the position?
- If an opposite scenario becomes stronger after entry, should the system reduce, hedge, or only manage stop/TP?
- Can stops move after fill?
- Can exits happen in multiple locations?
- Is partial exit part of scenario logic or position management?
- If several entries exist inside one zone, are they separate positions or one position bucket?
- If max lot was split into multiple orders, are they separate trades or one logical position?
- Is hedging part of the same position logic or a separate entry logic?
- What states should the final transition model contain?

## Expected Output

```text
scenario_to_position_transition_v1
position_thread_model_v1
duplicate_reason_trade_block_v1
position_reason_lock_model_v1
multi_exit_state_v1
split_order_position_aggregation_v1
hedge_separate_entry_logic_policy_v1
```
