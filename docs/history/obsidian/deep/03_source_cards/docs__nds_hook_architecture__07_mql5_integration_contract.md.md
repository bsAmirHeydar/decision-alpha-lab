
---
type: source_card
source_path: "docs/nds_hook_architecture/07_mql5_integration_contract.md"
source_ext: ".md"
source_size: 1609
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "Rally", "Validation / Audit"]
entities: []
---

# Source Card — 07_mql5_integration_contract.md

## Source

[[docs/nds_hook_architecture/07_mql5_integration_contract|docs/nds_hook_architecture/07_mql5_integration_contract.md]]

## Summary

This file defines the implementation boundary for adding Hook display to the central expert. Recommended display selector: Recommended default: Rally-only mode must not call Hook rendering in a way that changes existing F-counting behavior. The Hook calculator should receive: It should output: The renderer should only draw. It must not decide trades. It must not create orders. It must not modify risk. Every Hook chart object must use a unique prefix. Suggested root: Optional CSV rows should be generated only when enabled. Suggested rows: If Hook calculation fails: This integration must not add:

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 07 — MQL5 Integration Contract
  - Purpose
  - Input Contract
  - Preservation Rule
  - Hook Calculation Contract
  - Hook Renderer Contract
  - Namespacing
  - Audit Contract
  - Failure Policy
  - No Execution Boundary

## Related Source Documents

- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `19`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|16_phase09_visual_smoke_test_harness_implementation.md]] — score `19`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `18`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `17`
- [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|17_phase10_freeze_training_contract_implementation.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
