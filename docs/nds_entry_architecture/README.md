---
title: NDS Entry Transition Architecture
status: implemented_scaffold_plus_phase52
version: 1.0.0
updated: 2026-07-10
---
# NDS Entry Transition Architecture

## Mission

This package creates a deterministic bridge from the existing NDS market-anatomy engine to future trade setup and execution layers:

```text
Valid Hook Structure
→ Zone Contract
→ Setup Candidate
→ Trade Plan
→ Broker-Neutral Command Preview
→ Future Execution Adapter
```

Phase 51 remains intentionally **no-send**. Phase 52 adds a separate, narrow, opt-in execution profile for the explicit HH/F3H Hook-terminal limit and same-direction F123 exit contract. The general Zone adapter and generic command preview remain fail-closed.

## Why a separate NDS entry layer is required

Phoenix already contains generic Level 20–30 research and broker-preview modules. Those modules consume generic visible F/Hook objects and therefore must not be treated as the final NDS entry doctrine. NDS requires a stricter source contract:

1. the source must be a canonical valid Hook family;
2. the Hook must satisfy the selected closure gate;
3. Zone construction must come from the approved Zone Canon;
4. Hook direction and trade direction must remain separate;
5. Setup, Trade Plan, Command, Risk, and Broker authority must remain separate objects;
6. unresolved doctrine must block rather than silently invent geometry.

## Implemented modules

```text
FP_NDSStructureSnapshot.mqh
FP_NDSEntryTypes.mqh
FP_NDSEntryRules.mqh
FP_NDSEntryExport.mqh
FP_NDSEntryEngine.mqh
```

## Output files

When enabled, the central EA writes:

```text
MQL5/Files/FlagCountingPhoenix/nds_entry_structure_snapshot.csv
MQL5/Files/FlagCountingPhoenix/nds_entry_setup_candidate.csv
MQL5/Files/FlagCountingPhoenix/nds_entry_trade_plan.csv
MQL5/Files/FlagCountingPhoenix/nds_entry_command_preview.csv
MQL5/Files/FlagCountingPhoenix/nds_entry_pipeline_summary.csv
```

## Safe default

The default profile is:

```text
FP_NDS_ENTRY_PROFILE_PRE_CANON_BLOCKED
```

This means the code can observe and export the latest eligible valid Hook, but it cannot create a canonical Zone, ready Trade Plan, or sendable command until the remaining Hook/Zone/Entry decisions are locked.

## Reading order

1. [[01_doctrine_and_authority]]
2. [[02_structure_to_setup_contract]]
3. [[03_zone_adapter_contract]]
4. [[04_setup_state_machine]]
5. [[05_trade_plan_contract]]
6. [[06_command_preview_contract]]
7. [[07_risk_and_capital_boundary]]
8. [[08_data_and_audit_schema]]
9. [[09_mql5_module_architecture]]
10. [[10_validation_and_release_plan]]
11. [[11_canon_question_backlog]]
12. [[12_implementation_roadmap]]
13. [[13_operator_profiles]]
14. [[phase52_hook_limit_f123_execution/README|Phase 52 Hook Limit and F123 Exit]]

## Non-negotiable boundary

```text
No Zone Canon → no canonical Setup
No trade-direction doctrine → no directional Trade Plan
No locked entry/stop/target contract → no command preview
No independent risk and broker authorization → no live execution
```

## Obsidian map

```text
docs/obsidian_hook/00_mocs/NDS_ENTRY_EXECUTION_MOC.md
```


## Phase 52 executable overlay

The opt-in overlay is documented at:

```text
docs/nds_entry_architecture/phase52_hook_limit_f123_execution/
```

It is source-restricted to valid HH/F3H Hooks, uses a terminal-price pending limit, enforces one managed exposure by magic across charts, and closes only after a new full same-direction F123 chain. Both live-authority inputs default to false.


## Phase 53 — Lightweight backtest runtime

The dedicated Strategy Tester executable and its shared-core parity contract are documented in:

```text
phase53_lightweight_backtest/README.md
```
## Phase 54 — NDS × CG AI cycle-selection architecture

The research-only architecture for discovering non-random and non-simultaneous CG/cycle relationships is documented in:

```text
../nds_ai_cycle_selection/README.md
```

Phase 54 adds schemas, anti-random evidence gates, walk-forward design, and a no-training research scaffold. It does not change the executable Phase 52/53 strategy.

## F2 Waist-Break Point-2 — dedicated lightweight profile

The corrected canonical setup is documented at:

```text
f2_waist_break_point2_limit/README.md
```

It reuses Phoenix canonical node/F1/F2 builders but does not wait for F2 confirmation. A complete unconfirmed F2 body arms a limit strictly beyond the F2 Waist. The Waist is Point 1; the limit fill is executable Point 2; Stop is strictly beyond the direct parent F1 Waist; Target is the F2 Leg2 endpoint. The dedicated entry-timeframe detector builds no Hook branches and skips visual/canonical post-processing. The optional higher-timeframe authority gate is separate and runs a cached canonical F/Hook phase pass only on new HTF bars. The executable now also supports a minimum Reward/Risk gate, opposite-direction hedge contexts, and independent same-direction contexts. Parallel same-symbol positions are permitted only on MT5 hedging accounts.


## F2 v5 — overlap arbitration and RR entry repricing

The dedicated F2 Waist-Break Point-2 backtest now reprices sub-threshold RR setups by moving only the pending Entry toward the fixed F1-waist Stop, and deduplicates near-identical same-direction contexts using configurable stop-corridor overlap. The default overlap threshold is 80%, with the wider executable corridor selected. See `docs/nds_entry_architecture/f2_waist_break_point2_limit/11_overlap_arbitration_and_rr_entry_repricing.md`.

The profile now also supports two explicit exit modes. Fixed mode attaches TP at the original F2 Leg2. Dynamic F3-retest mode keeps that same F2 Leg2 only as the RR reference, waits for the exact source F2 confirmation node (canonical F3 Leg1), observes a correction, and exits on the retest of that node. The full contract is in `docs/nds_entry_architecture/f2_waist_break_point2_limit/12_dual_exit_fixed_f2_and_f3_flag_retest.md`.


## F2 v7 — higher-timeframe F-phase direction filter

The F2 Point-2 profile now contains an entry-authority gate based on the canonical higher-timeframe phase. Default `H1` bullish F authorizes only Buy setups; bearish F authorizes only Sell setups; Hook/ND or unresolved state blocks new orders. The full contract is in `f2_waist_break_point2_limit/13_higher_timeframe_f_phase_direction_filter.md`.

## Exact per-trade F3 lineage exit

The F2 Waist-Break profile now resolves dynamic exits through `Position → Source F2 → Direct Child F3`. The direct child F3 Waist is the correction gate and that child's Leg1 is the target. Cross-context target borrowing is fail-closed.


## F2 v9 — higher-timeframe F3 exit

The F2 Point-2 profile now has a third exit mode. A lower-timeframe position can be held until the first eligible canonical same-direction F3 on a configurable higher timeframe forms Leg1 and then its own Waist; TP is armed at that exact Leg1 endpoint. The default exit timeframe is H1. RR remains anchored to the original lower-timeframe F2 Leg2. See `f2_waist_break_point2_limit/15_higher_timeframe_f3_flag_retest_exit.md`.


## F2 v10 — higher-timeframe F1-to-F2 confirmation window

The optional higher-timeframe entry gate is evaluated independently across every canonical HTF count. The default-on lifecycle window qualifies a count only after its exact F1 confirmation and strictly before confirmation of its exact direct-child F2. At least one sole-direction count may authorize entry; opposite qualifying directions remain fail-closed. Hook/ND veto is count-local. See `f2_waist_break_point2_limit/16_higher_timeframe_f1_to_f2_confirmation_window.md`.

## F2 canonical frequency recovery — version 2.00

The F2 setup is now lifecycle-owned instead of restricted to its first observable bar. Pending attempts are consumed on fill by default, unrelated HTF Hooks no longer globally veto all counts, F1/F2 confirmation boundaries no longer depend on spawn eligibility, FAST coverage includes 800 bars and L=8, and parallel-context tests can fail fast on non-hedging accounts. Causal missed-entry and target-consumption checks prevent retrospective orders. See `f2_waist_break_point2_limit/17_canonical_frequency_recovery_and_lifecycle.md`.
