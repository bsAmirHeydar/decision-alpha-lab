# NDS F2 Waist-Break Point-2 Limit Setup

## Status

Canonical execution contract for the dedicated lightweight Strategy Tester profile.

The setup has three explicit exit modes and an optional canonical higher-timeframe F-phase direction filter. The filter is enabled by default on H1. Every canonical HTF count is evaluated independently, and the default-on lifecycle window authorizes a direction when at least one count is after its own F1 confirmation and before confirmation of its exact direct-child F2. Opposite qualifying directions remain fail-closed.

## Core sentence

Phoenix already owns the complete F2 lifecycle: a two-leg flag body, a post-flag internal 1/2 or Waist-break branch, and a later favorable return through the original flag end that confirms F2. This execution profile does not redefine that lifecycle. It projects the preferred Waist-break branch by staging a strict limit beyond the already-existing F2 flag Waist after the body is observable, so the fill captures executable Point 2 while the F engine continues unchanged. Stop remains beyond the direct parent F1 Waist, and the original F2 flag end remains the fixed target and RR reference.

## Index

1. [Canonical setup contract](01_canonical_setup_contract.md)
2. [Structural anatomy](02_structural_anatomy.md)
3. [Execution state machine](03_execution_state_machine.md)
4. [Price and order semantics](04_price_and_order_semantics.md)
5. [Lifecycle and edge cases](05_lifecycle_and_edge_cases.md)
6. [Module architecture](06_module_architecture.md)
7. [Validation and acceptance](07_validation_and_acceptance.md)
8. [Operator guide](08_operator_guide.md)
9. [Correction of the previous implementation](09_previous_implementation_correction.md)
10. [Reward/Risk and parallel-context policy](10_reward_risk_and_parallel_context_policy.md)
11. [Overlap arbitration and RR entry repricing](11_overlap_arbitration_and_rr_entry_repricing.md)

12. [Dual exit contract: fixed F2 end or F3 flag retest](12_dual_exit_fixed_f2_and_f3_flag_retest.md)
13. [Higher-timeframe F-phase direction filter](13_higher_timeframe_f_phase_direction_filter.md)
14. [Exact per-trade F3 lineage exit](14_exact_per_trade_f3_lineage_exit.md)

15. [Higher-timeframe F3 flag-retest exit](15_higher_timeframe_f3_flag_retest_exit.md)
16. [Higher-timeframe F1-to-F2 confirmation window](16_higher_timeframe_f1_to_f2_confirmation_window.md)
17. [Canonical frequency recovery and lifecycle corrections](17_canonical_frequency_recovery_and_lifecycle.md)
18. [Canonical Point-2 projection root fix](18_canonical_point2_projection_root_fix.md)
