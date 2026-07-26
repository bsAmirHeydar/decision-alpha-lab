
---
type: source_card
source_path: "docs/nds_hook_architecture/01_scope_and_inputs.md"
source_ext: ".md"
source_size: 1588
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "Rally", "Validation / Audit"]
entities: []
---

# Source Card — 01_scope_and_inputs.md

## Source

[[docs/nds_hook_architecture/01_scope_and_inputs|docs/nds_hook_architecture/01_scope_and_inputs.md]]

## Summary

Add Hook visualization and diagnostics to the same central expert that already displays Rally / F-counting. The existing Rally behavior must remain untouched. Recommended input enum: The default should preserve existing behavior: This ensures that adding Hook code does not change the existing F-counting / Rally display. Use the current F-counting logic exactly as it is. No Hook code should change the Rally calculation path. Draw CycleHook / Hook objects and diagnostics. Do not draw Rally/F-counting labels unless they are explicitly needed for Hook debug. Draw both layers. Object names must be namespaced to avoid overwriting existing Rally chart objects. Suggested object prefixes: The first implementation should be visual and audit-only. No trading behavior.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 01 — Scope and Inputs
  - Objective
  - Display Family Input
  - Suggested User Inputs
  - Default Behavior
  - Display Modes
    - Rally Only
    - Hook Only
    - Rally and Hook
  - Object Namespace
  - First Implementation Goal

## Related Source Documents

- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `13`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `13`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `13`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `13`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `13`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `13`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
