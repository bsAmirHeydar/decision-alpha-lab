# Index Fragment — ENT-R04

## ENT-R04 — After Fill: Scenario-to-Position Transition

Path:

```text
docs/experience_capture/answers/ENT-R04/
```

Summary:

After a limit entry is filled, the trade becomes an active PositionThread linked to the same scenario, zone, entry extreme, and reason set that created it. While that position is open, the system must not take another duplicate trade with the same reasons. The reason set is locked to the open position until the position is closed or completed. Exits can occur in multiple places according to NDS exit and destination logic. Hedging is a separate topic because it requires separate entry logic and should not be automatically triggered by the existence of an active position or an opposite scenario.

Main derived architecture requirements:

```text
scenario_to_position_transition_v1.csv
position_thread_model_v1.csv
duplicate_reason_trade_block_v1.csv
position_reason_lock_model_v1.csv
multi_exit_state_v1.csv
split_order_position_aggregation_v1.csv
hedge_separate_entry_logic_policy_v1.csv
position_lineage_ledger_v1.csv
```
