
---
type: source_card
source_path: "docs/nds_hook_architecture/26_phase18_minimal_readability_qualified_hooks.md"
source_ext: ".md"
source_size: 1606
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Hook"]
entities: []
---

# Source Card — 26_phase18_minimal_readability_qualified_hooks.md

## Source

[[docs/nds_hook_architecture/26_phase18_minimal_readability_qualified_hooks|docs/nds_hook_architecture/26_phase18_minimal_readability_qualified_hooks.md]]

## Summary

`MINIMAL_ALL_HOOKS` correctly removed the heavy P03/P04/P05/P06 overlays, but the chart was still visually busy because it rendered every raw candidate, including many `X1` structures. An `X1` structure is useful for raw… The arc height was also too large on high-range moves, and arrow-style X markers still added unnecessary visual weight. Phase 18 adds readability controls to Phase 02: `FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS` now forces: So the view shows all **qualified** Hook sequences, not every one-node candidate. `X1` candidates are hidden by default. `X2+` Hook structures remain visible. Arcs are capped so they do not dominate the chart. Nodes use small neutral dot markers rather than directional arrow glyphs. Node numbers are offset slightly from the node price so they are readable. Set:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 18 — Minimal Readability / Qualified Hooks
  - Problem
  - Fix
  - Minimal profile defaults
  - Meaning
  - To show every raw candidate again

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
