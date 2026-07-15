# 03 — Profile Contract and Locked Parameters

## Contract

The profile is identified by:

```text
profile = HOOK_864_CYCLE_R1
schema_version = nds_hook_864_cycle_r1_v1
```

Its semantic parameters are locked:

| Parameter | Required value | Failure reason |
|---|---:|---|
| Hook entry ratio | `0.864` | `approved_hook_entry_ratio_must_be_exactly_0_864` |
| minimum X count | `3` | `approved_node_count_window_must_be_exactly_3_to_4` |
| maximum X count | `4` | same |
| confirmed terminal gate | `true` | `confirmed_terminal_gate_must_remain_enabled` |
| untouched level gate | `true` | `untouched_86_4_gate_must_remain_enabled` |
| reward multiple | `1.0` | `approved_fixed_reward_must_be_exactly_1R` |

## Why inputs remain exposed

The central and tester EAs expose these values so a run manifest can record them and a modified `.set` file fails explicitly. They are not optimization parameters. Changing a value blocks setup construction instead of silently creating a different strategy under the same name.

## Compatibility default

`FP_ResetNDSHookTradeConfig` selects `TERMINAL_F123`. Therefore existing installations retain Phase 52 behavior until an operator deliberately chooses the new enum.

## Profile-specific outputs

The setup records profile label, canonical X count, Origin, Crown, Terminal, terminal retracement, entry ratio, first-arrival decision, normalized Entry/Stop/Target, risk distance, reward distance, and realized R. This prevents an analyst from confusing Phase 52 rows with Phase 55 rows.
