
---
type: source_card
source_path: "docs/nds_hook_architecture/30_phase22_arc_gray_sequence_number_colors.md"
source_ext: ".md"
source_size: 1425
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook"]
entities: []
---

# Source Card — 30_phase22_arc_gray_sequence_number_colors.md

## Source

[[docs/nds_hook_architecture/30_phase22_arc_gray_sequence_number_colors|docs/nds_hook_architecture/30_phase22_arc_gray_sequence_number_colors.md]]

## Summary

Align the minimal Hook rendering with the intended visual semantics: the cycle arc represents the overall Hook envelope from origin to the Hook's own directional extreme the cycle arc should be a dim low-contrast gray, close to black node numbers should show **all visible sequence memberships** within one sequence, all node numbers should share the **same sequence color** different sequences should use different number colors label collisions at the same node should remain stacked vertically for readability A new Phase 02 flag was added: In the minimal all-hooks profile this is forced to `false`, and the arc color is forced to a dim near-black gray: So the semicircle no longer inherits the sequence palette color. In the minimal all-hooks profile: `color_node_labels_with_sequence = true` `color_node_numbers_by_index = false` `use_sequence_palette_colors = true` So every number belonging t

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 22 — Gray Cycle Arcs and Sequence-Colored Number Labels
  - Goal
  - What changed
    - Fixed gray cycle arcs
    - Sequence-colored numbers
    - Collision stacking preserved

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
