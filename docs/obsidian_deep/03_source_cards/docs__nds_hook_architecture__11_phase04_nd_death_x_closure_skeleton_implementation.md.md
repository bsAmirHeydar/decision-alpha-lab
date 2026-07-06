
---
type: source_card
source_path: "docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation.md"
source_ext: ".md"
source_size: 2586
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 11_phase04_nd_death_x_closure_skeleton_implementation.md

## Source

[[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation.md]]

## Summary

Phase 04 adds lifecycle diagnostics to the CycleHook architecture: This phase still does not add Hook Type A/B/C. Phase 02 created X sequences. Phase 03 created Y opposite Extremes. Phase 04 uses those objects to create a visible lifecycle skeleton before final type classification and full closure logic. This is still a skeleton. It exposes lifecycle states and thresholds for audit. It does not yet produce a trade signal and does not send orders. Phase 04 treats ND as a return-toward-origin candidate. Given the Phase 02 sequence definitions: The default ND threshold is 50% of the distance from the latest X node back toward origin. Phase 04 draws a death/origin boundary at the origin price. If the return goes through origin, the record is marked as: This is a lifecycle diagnostic. Phase 04 uses the latest available Y reference: For closure, the default requirement is: Then it calculates a

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton
  - Phase Goal
  - Why This Phase Exists
  - Important Interpretation
  - ND Candidate
  - Death / Origin Return Penetration
  - X Closure Skeleton
  - Lifecycle States
  - Chart Objects
  - CSV Outputs
  - Deferred to Future Phases
  - No Execution Boundary

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `18`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `15`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `15`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `15`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `15`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `15`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `15`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
