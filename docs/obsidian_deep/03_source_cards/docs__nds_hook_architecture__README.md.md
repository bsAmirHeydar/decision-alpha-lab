
---
type: source_card
source_path: "docs/nds_hook_architecture/README.md"
source_ext: ".md"
source_size: 2755
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Market Anatomy", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — README.md

## Source

[[docs/nds_hook_architecture/README|docs/nds_hook_architecture/README.md]]

## Summary

This documentation freezes the Hook architecture before implementation. The implementation target is the central expert that already performs Rally / F-counting. The existing Rally mode must remain unchanged. Hook rendering and Hook diagnostics should be added as a parallel display family. Add a display selector to the central expert: Expected behavior: This is visualization and structural diagnostics only. Do not add execution logic, broker requests, order sending, volume sizing, risk sizing, or live trading behavior. Hook and CycleHook are the same algorithmic object. The Hook layer must be built from the same NDS anatomy: Hook must become infrastructure like F-counting. The system should be built in layers: Phase 10 implements the Hook v1 freeze and training contract. It does not draw new Hook structure. It checks Phase 08 audit state, Phase 09 visual smoke state, Phase 06 quality rec

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- NDS Hook Architecture — Design Pack
  - Primary Integration Goal
  - Non-Negotiable Boundary
  - Core NDS Rule
  - Build Philosophy
  - Implemented overlays
  - Implementation overlay note — Phase 10

## Related Source Documents

- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `27`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|16_phase09_visual_smoke_test_harness_implementation.md]] — score `27`
- [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|17_phase10_freeze_training_contract_implementation.md]] — score `27`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `27`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `25`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `25`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `23`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `23`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11_phase04_nd_death_x_closure_skeleton_implementation.md]] — score `21`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
