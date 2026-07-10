---
title: NDS Entry Transition Architecture
status: implemented_scaffold
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

The implemented layer is intentionally **no-send**. It prepares state, schemas, adapters, audit output, and command envelopes without granting broker or capital authority.

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
