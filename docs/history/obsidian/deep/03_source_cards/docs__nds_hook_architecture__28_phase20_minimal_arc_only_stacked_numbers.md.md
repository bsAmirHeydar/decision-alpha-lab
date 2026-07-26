
---
type: source_card
source_path: "docs/nds_hook_architecture/28_phase20_minimal_arc_only_stacked_numbers.md"
source_ext: ".md"
source_size: 1759
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook"]
entities: []
---

# Source Card — 28_phase20_minimal_arc_only_stacked_numbers.md

## Source

[[docs/nds_hook_architecture/28_phase20_minimal_arc_only_stacked_numbers|docs/nds_hook_architecture/28_phase20_minimal_arc_only_stacked_numbers.md]]

## Summary

Refine the minimal Hook rendering so it matches the intended reading style: no straight line segments between Hook nodes only the semi-circular cycle arc should be drawn node numbers should use distinct colors by number (`1`, `2`, `3`, `4`) if the same chart node participates in multiple sequences, its numbers should be stacked vertically in a clean column origin stays visually marked but unlabeled in the minimal number mode In `FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS`: `draw_x_lines = false` `draw_cycle_arc = true` So the minimal view no longer connects `origin -> X1 -> X2 -> X3 -> X4` with direct straight segments. Phase 02 now supports dedicated colors for numeric node labels: `node1_label_color` `node2_label_color` `node3_label_color` `node4_label_color` And a switch: When multiple sequences place labels on the same node/time-price anchor, the labels are no longer drawn on top of one anot

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 20 — Minimal Arc-Only View with Stacked Number Labels
  - Goal
  - What changed
    - Arc-only minimal view
    - Distinct colors by node number
    - Clean vertical stacking on collisions
  - Minimal profile defaults

## Related Source Documents

- [[docs/nds_hook_architecture/01_scope_and_inputs|01_scope_and_inputs.md]] — score `7`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04_x_y_closure_and_hook_types.md]] — score `7`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05_visualization_and_diagnostics.md]] — score `7`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `7`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11_phase04_nd_death_x_closure_skeleton_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12_phase05_hook_type_abc_classifier_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `7`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
