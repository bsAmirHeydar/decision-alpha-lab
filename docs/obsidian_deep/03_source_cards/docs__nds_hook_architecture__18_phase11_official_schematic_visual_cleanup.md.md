
---
type: source_card
source_path: "docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup.md"
source_ext: ".md"
source_size: 2144
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook", "Rally"]
entities: []
---

# Source Card — 18_phase11_official_schematic_visual_cleanup.md

## Source

[[docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup|docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup.md]]

## Summary

The raw multi-phase Hook overlay was technically correct for debugging, but visually too noisy for the official structural reading. The main pollution came from: projecting lifecycle thresholds all the way to `TimeCurrent()` stacking full debug labels from Phase 05 and Phase 06 leaving the Phase 07 view profile on permissive modes such as `KEEP_INPUTS` drawing too many structures at once A new Phase 07 view profile was added: `FP_HOOK_P07_VIEW_OFFICIAL_SCHEMATIC` This profile draws a clean Hook schematic: Phase 02: origin + X nodes + X lines Phase 03: Y extremes + Y lines Phase 04: ND / death / X-close markers only Phase 05: compact Hook type anchor + compact type label Phase 06: compact quality anchor + compact quality label It intentionally hides: Phase 02 labels Phase 03 labels and X-reference clutter Phase 04 threshold bands and lifecycle debug labels Phase 05 comparison lines and de

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]]

## Entities

—

## Headings

- NDS Hook Official Schematic Visual Cleanup
  - Why
  - What changed
    - 1) New official visual profile
    - 2) New clean defaults
    - 3) Threshold-line fix
    - 4) Compact labels
  - Recommended usage

## Related Source Documents

- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `11`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `11`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
