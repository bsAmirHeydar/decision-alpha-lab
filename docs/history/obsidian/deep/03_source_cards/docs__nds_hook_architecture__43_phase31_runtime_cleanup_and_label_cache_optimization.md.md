
---
type: source_card
source_path: "docs/nds_hook_architecture/43_phase31_runtime_cleanup_and_label_cache_optimization.md"
source_ext: ".md"
source_size: 1376
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook"]
entities: []
---

# Source Card — 43_phase31_runtime_cleanup_and_label_cache_optimization.md

## Source

[[docs/nds_hook_architecture/43_phase31_runtime_cleanup_and_label_cache_optimization|docs/nds_hook_architecture/43_phase31_runtime_cleanup_and_label_cache_optimization.md]]

## Summary

Reduce unnecessary runtime work without changing Hook behavior, visual semantics, default outputs, or no-trade boundaries. This phase does not remove features and does not alter Hook lifecycle rules. It only avoids repeated work that produced the same result. Phase 30 made label spacing responsive by reading local candle ranges around every label anchor. When many labels share nearby bars, repeatedly calling `iBarShift`, `iHigh`, and `iLow` for the same anchors is unnecessary… Phase 31 adds per-render caches for: `datetime -> bar shift` `(bar shift, lookback) -> average local range points` The cache is reset at the start of each Hook draw pass, so it cannot go stale across timeframe changes or redraws. Previous lifecycle cleanup scanned all chart objects once per prefix. With many Hook prefixes this could scan the chart 10+ times. Phase 31 adds a single-pass prefix cleanup function: This

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 31 — Runtime Cleanup and Responsive Label Cache Optimization
  - Goal
  - What was optimized
    - 1) Responsive label distance caching
    - 2) Batch cleanup by prefixes
  - Behavior guarantee

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
