
---
type: source_card
source_path: "docs/nds_hook_architecture/41_phase29_bar_index_arc_and_vertical_label_stacks.md"
source_ext: ".md"
source_size: 1378
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Hook"]
entities: []
---

# Source Card — 41_phase29_bar_index_arc_and_vertical_label_stacks.md

## Source

[[docs/nds_hook_architecture/41_phase29_bar_index_arc_and_vertical_label_stacks|docs/nds_hook_architecture/41_phase29_bar_index_arc_and_vertical_label_stacks.md]]

## Summary

Fix two visual issues in the minimal Hook view: Hook envelope curves should be laid out by candle progression rather than naive wall-clock interpolation, so the arc follows chart bar spacing more faithfully and does not visually break across session gaps. Hook/branch labels should stack in cleaner vertical columns above peaks and below valleys instead of colliding on top of each other. The Hook envelope renderer now prefers bar-index aligned interpolation. start, crown, and end anchor times are converted to chart bar shifts the curve is sampled along bar progression between those anchors each short trend segment is anchored on actual chart bar times This makes the gray Hook envelope follow the chart's candle cadence more closely. Label stacking is now clustered by: side (above peaks / below valleys) bar distance optional time distance fallback price proximity This makes labels form more

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 29 — Bar-Index Arc Timing and Vertical Label Stacks
  - Goal
  - Changes
    - 1) Arc timing aligned to bar index
    - 2) Stronger label clustering
  - New config knobs
  - Default profile updates

## Related Source Documents

- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05_visualization_and_diagnostics.md]] — score `7`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `7`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12_phase05_hook_type_abc_classifier_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/40_phase28_lifecycle_cleanup_clustered_ids|40_phase28_lifecycle_cleanup_clustered_ids.md]] — score `7`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `6`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
