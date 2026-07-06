
---
type: source_card
source_path: "docs/nds_hook_architecture/32_phase23_hook_origin_group_semicircle.md"
source_ext: ".md"
source_size: 1381
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Hook"]
entities: []
---

# Source Card — 32_phase23_hook_origin_group_semicircle.md

## Source

[[docs/nds_hook_architecture/32_phase23_hook_origin_group_semicircle|docs/nds_hook_architecture/32_phase23_hook_origin_group_semicircle.md]]

## Summary

The previous implementation still drew a cycle arc **per sequence**. Even with straight X-lines disabled, this produced multiple overlapping arc traces that visually looked like node-to-node connections. That is not the intended Hook schematic. Node numbering should show **all sequences**. But the cycle semicircle should represent the **Hook envelope**, not each inner sequence leg separately. Therefore the cycle arc should be drawn **once per Hook origin group**. A Hook-origin group is defined by: `direction` `origin_time` `origin_price` All selected sequences that share those fields belong to the same Hook envelope group. For each origin group: start = Hook origin end = directional extreme across all X points (`X1..X4`) of all sequences in the group positive Hook ⇒ lowest valley reached by the group negative Hook ⇒ highest peak reached by the group per-sequence cycle arcs are suppressed

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 23 — Hook-Origin Grouped Cycle Semicircle
  - Problem
  - Intended semantics
  - Grouping rule
  - Group arc endpoint
  - Rendering behavior
  - New input

## Related Source Documents

- [[docs/nds_hook_architecture/01_scope_and_inputs|01_scope_and_inputs.md]] — score `5`
- [[docs/nds_hook_architecture/02_cyclehook_object_model|02_cyclehook_object_model.md]] — score `5`
- [[docs/nds_hook_architecture/03_sequence_builder|03_sequence_builder.md]] — score `5`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04_x_y_closure_and_hook_types.md]] — score `5`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05_visualization_and_diagnostics.md]] — score `5`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `5`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07_mql5_integration_contract.md]] — score `5`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `5`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
