
---
type: source_card
source_path: "docs/nds_hook_architecture/02_cyclehook_object_model.md"
source_ext: ".md"
source_size: 2169
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Hook", "Rally", "UI / React"]
entities: []
---

# Source Card — 02_cyclehook_object_model.md

## Source

[[docs/nds_hook_architecture/02_cyclehook_object_model|docs/nds_hook_architecture/02_cyclehook_object_model.md]]

## Summary

Hook and CycleHook are the same algorithmic object. Recommended canonical object: There are two directions: A positive CycleHook starts from a valley. Its counted X nodes are valleys. The sequence is strictly lower valleys. Equal nodes are not accepted as new lower nodes. A negative CycleHook starts from a peak. Its counted X nodes are peaks. The sequence is strictly higher peaks. Equal nodes are not accepted as new higher nodes. One-point penetration of the origin kills the CycleHook. There is no structural buffer for validity. Execution buffer may exist later, but structural validity is strict. For a positive CycleHook, opposite Extremes are highs. For a negative CycleHook, opposite Extremes are lows. The opposite Extreme is used for: L starts from 2. L1 is not structurally meaningful for this Hook layer. Suggested fields: Suggested states:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- 02 — CycleHook Object Model
  - Canonical Rule
  - Directions
  - Positive CycleHook
  - Negative CycleHook
  - Death Rule
  - Opposite Extreme
  - Minimum L
  - CycleHook Fields
  - Lifecycle States

## Related Source Documents

- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `11`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|16_phase09_visual_smoke_test_harness_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/README|README.md]] — score `11`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
