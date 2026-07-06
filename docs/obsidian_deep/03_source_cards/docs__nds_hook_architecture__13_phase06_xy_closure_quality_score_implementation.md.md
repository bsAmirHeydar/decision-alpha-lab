
---
type: source_card
source_path: "docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation.md"
source_ext: ".md"
source_size: 4401
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 13_phase06_xy_closure_quality_score_implementation.md

## Source

[[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation.md]]

## Summary

Phase 06 adds an independent X/Y closure-strength and structural quality layer on top of Phase 05. It uses: This phase is still visualization and diagnostics only. Hook Type A/B/C is a global structural classifier. X/Y closure quality is a different layer: This separation is required because a Hook can be Type A/B/C while still having weak or incomplete internal X/Y closure. For positive CycleHook: Positive Y checks: For negative CycleHook: Negative Y checks: This is intentionally different from Hook Type A/B/C logic. Phase 06 reads the Phase 04 lifecycle fields: Default policy: So `XY_CLOSED` requires real Phase 04 `x_closed`, not just a candidate. Phase 06 emits: Meaning: Phase 06 computes: Default weights: Default buckets: Phase 06 draws objects with: Objects include: If enabled: The row-level CSV includes: Default display family remains: So Rally/F-counting behavior remains unchanged

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- 13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score
  - Phase Goal
  - Why This Phase Exists
  - Y-Sequence Closure Logic
  - X Closure Input
  - XY Closure States
  - Quality Score
  - New MQL5 Modules
  - New Expert Inputs
  - Chart Objects
  - CSV Outputs
  - Preservation Rules

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `22`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `21`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `21`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `21`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `21`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `20`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `20`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `20`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `20`
- [[docs/experience_capture/answers/NDS-R01/notes_en|notes_en.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
