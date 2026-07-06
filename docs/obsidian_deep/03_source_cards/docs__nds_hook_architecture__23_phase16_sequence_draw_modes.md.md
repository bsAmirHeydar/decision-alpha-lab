
---
type: source_card
source_path: "docs/nds_hook_architecture/23_phase16_sequence_draw_modes.md"
source_ext: ".md"
source_size: 1706
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Hook"]
entities: []
---

# Source Card — 23_phase16_sequence_draw_modes.md

## Source

[[docs/nds_hook_architecture/23_phase16_sequence_draw_modes|docs/nds_hook_architecture/23_phase16_sequence_draw_modes.md]]

## Summary

Phase 15 made the sequence inspector too strict by hard-capping `SEQUENCE_CYCLE_DEBUG` to a single sequence. That solved clutter, but it also hid the surrounding sequence-counting context. Phase 16 adds explicit draw modes so the Hook inspector can show more than one sequence without returning to the previous P05/P06/P04 label pileup. Modes: Direction filter: Scale filter: `SEQUENCE_CYCLE_DEBUG` no longer hard-caps visible sequences to 1. It uses `InpHookPhase07MaxSequencesToDraw` and Phase 02 draw-mode filters while still hard-disabling P03/P04/P05/P06 drawing.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 16 — Sequence Draw Modes
  - Reason
  - New Phase 02 input
  - Supporting inputs
  - Recommended views
    - Balanced context
    - One scale inspection
    - Exact sequence inspection
  - Phase 07 interaction

## Related Source Documents

- [[docs/nds_hook_architecture/01_scope_and_inputs|01_scope_and_inputs.md]] — score `5`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04_x_y_closure_and_hook_types.md]] — score `5`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05_visualization_and_diagnostics.md]] — score `5`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `5`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11_phase04_nd_death_x_closure_skeleton_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12_phase05_hook_type_abc_classifier_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `5`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
