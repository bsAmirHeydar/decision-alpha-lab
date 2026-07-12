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

It reuses Phoenix canonical node/F1/F2 builders but does not wait for F2 confirmation. A complete unconfirmed F2 body arms a limit strictly beyond the F2 Waist. The Waist is Point 1; the limit fill is executable Point 2; Stop is strictly beyond the direct parent F1 Waist; Target is the F2 Leg2 endpoint. The dedicated detector builds no Hook branches and skips all visual/canonical post-processing. The executable now also supports a minimum Reward/Risk gate, opposite-direction hedge contexts, and independent same-direction contexts. Parallel same-symbol positions are permitted only on MT5 hedging accounts.
