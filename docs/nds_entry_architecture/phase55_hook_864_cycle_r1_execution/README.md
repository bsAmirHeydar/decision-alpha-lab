---
title: NDS Phase 55 Hook 86.4 Cycle R1 Execution
status: implemented_opt_in_reference_qa_pending_metaeditor
version: 1.2.0
updated: 2026-07-16
---
# NDS Phase 55 — Hook 86.4 Cycle R1 Execution

## Purpose

Phase 55 adds one narrow execution profile to the existing NDS Hook trade stack. It does not create a new Hook detector, a new node counter, a new cycle object, or a second execution engine.

```text
Canonical FP_HookPhase02Sequence
→ existing valid-family and confirmed-terminal gates
→ canonical x_count ∈ {3,4}
→ existing Phase03 Y-axis builder
→ existing Phase04 50% X-closure lifecycle
→ closed-bar first-arrival proof after closure
→ limit at crown-to-origin 86.4%
→ stop behind canonical cycle death boundary
→ attached target at exactly 1R
→ existing sizing, one-exposure, persistence, broker, and audit layers
```

## Approved profile identity

```text
FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1
schema = nds_hook_864_cycle_r1_v2
entry_ratio = 0.864
x_count = 3 or 4
require_confirmed_terminal = true
require_phase04_x_closed = true
closure_ratio = 0.50
require_level_untouched_after_closure = true
reward_r = 1.0
```

These values are not optimization knobs. Inputs remain visible for evidence and reproducibility, but the profile validator rejects any noncanonical value.

## Compatibility

`FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123` remains enum value `0`, remains the reset/default profile, continues to enter at `resolve_price`, continues to attach no fixed TP, and continues to close on a new same-direction F123 chain. Phase 55 is opt-in and isolated by profile dispatch and a dedicated ledger schema.

## Reading order

1. [[01_scope_authority_and_non_goals]]
2. [[02_authoritative_reuse_map]]
3. [[03_profile_contract_and_locked_parameters]]
4. [[04_cycle_close_and_x3_x4_eligibility]]
5. [[05_hook_864_entry_geometry]]
6. [[06_stop_target_and_broker_normalization]]
7. [[07_setup_identity_one_attempt_and_no_reprice]]
8. [[08_pending_position_and_exit_state_machine]]
9. [[09_risk_execution_and_authority_boundaries]]
10. [[10_audit_ledger_and_evidence_schema]]
11. [[11_python_reference_and_test_vectors]]
12. [[12_validation_and_hostile_test_matrix]]
13. [[13_operator_runbook]]
14. [[14_persian_strategy_doctrine]]
15. [[15_compatibility_migration_and_rollback]]
16. [[16_definition_of_done_limitations_and_residual_risk]]
17. [[17_no_trade_root_cause_and_engine_fix]]
18. [[18_phase04_closure_and_first_arrival_contract]]
19. [[19_v1_1_1_trade_action_compile_hotfix]]
20. [[20_exact_acceleration_and_maximum_speed_contract]]

## Implementation map

```text
FP_NDSHookTradeTypes.mqh
FP_NDSHook864CycleR1Evidence.mqh
FP_NDSHook864CycleR1EvidenceEngine.mqh
FP_NDSHook864CycleR1Rules.mqh
FP_NDSHookTradeRules.mqh
FP_NDSHookTradeExecutionCore.mqh
FP_NDSHookTradeExport.mqh
FP_NDSHookTradeEngine.mqh
FP_NDSBacktestEngine.mqh
FlagCountingPhoenixExperiment.mq5
NDSHookLimitF123Backtest.mq5
```

## Safe defaults

The central EA keeps both decision and broker authority disabled:

```text
InpNDSHookTradeEnabled = false
InpNDSHookTradeSendLiveOrders = false
InpNDSHookTradeProfile = TERMINAL_F123
```

Choosing the Phase 55 profile still does not send an order unless both authority inputs are deliberately enabled and all existing broker/risk gates pass.


## Dedicated tester defaults

The dedicated Strategy Tester expert now defaults to the intended low-frequency profile:

```text
Expert = NDSHookLimitF123Backtest
InpBTProfile = PARITY
InpBTTradeProfile = HOOK_864_CYCLE_R1
InpBTPrintRunSummary = true
```

The central EA remains fail-closed and unchanged by this diagnostic default.


## Exact acceleration v1.2

The PARITY universe remains 5000 closed bars across scales `2,3,5,8,13,21,34,55`. `InpBTExactAcceleration=true` skips only engines whose outputs cannot alter the current decision. See [[20_exact_acceleration_and_maximum_speed_contract]].
