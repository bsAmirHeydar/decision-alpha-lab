
---
type: source_card
source_path: "docs/nds_hook_architecture/25_phase17_minimal_all_hooks_view.md"
source_ext: ".md"
source_size: 1541
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook"]
entities: []
---

# Source Card — 25_phase17_minimal_all_hooks_view.md

## Source

[[docs/nds_hook_architecture/25_phase17_minimal_all_hooks_view|docs/nds_hook_architecture/25_phase17_minimal_all_hooks_view.md]]

## Summary

Show all Hook sequences in a minimal structural rendering: all Hook sequences sequence arc + path node markers only node numbers on chart node/line/arc colors derived from sequence color no long labels, no quality/type overlays, no thresholds This profile keeps only Phase 02 visible and disables Phase 03 through Phase 06. When `MINIMAL_ALL_HOOKS` is active: `Phase 02` remains enabled `draw_origin = true` `draw_x_nodes = true` `draw_x_lines = true` `draw_cycle_arc = true` `draw_sequence_count_label = false` `draw_labels = true` `use_sequence_palette_colors = true` `color_origin_with_sequence = true` `color_node_labels_with_sequence = true` `minimal_numbers_only = true` `node_label_mode = NUMBERS_FROM_ZERO` `sequence_draw_mode = RECENT_N` `max_sequences_to_draw = 0` (draw all filtered sequences) This produces a minimal view where each Hook sequence is color-coherent and the only text on th

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 17 — Minimal All Hooks View
  - Goal
  - New view profile
  - Minimal view behavior
  - New Phase 02 visual controls
  - Recommended inputs

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
