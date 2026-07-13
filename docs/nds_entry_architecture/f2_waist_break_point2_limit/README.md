# NDS F2 Waist-Break Point-2 Limit Setup

## Status

Canonical execution contract for the dedicated lightweight Strategy Tester profile.

The setup has two explicit exit modes and an optional canonical higher-timeframe F-phase direction filter. The filter is enabled by default on H1.

## Core sentence

After a complete two-leg F2 flag exists, the F2 waist is treated as structural Point 1. A strict penetration beyond that waist is Point 2. The system stages a limit order strictly beyond the F2 waist so the fill is the executable Point 2, places the stop beyond the direct parent F1 waist, and either targets the F2 Leg2 endpoint directly or, in dynamic mode, keeps that endpoint only as the RR reference and exits on the later F3 flag retest of the F2-confirmation node.

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
