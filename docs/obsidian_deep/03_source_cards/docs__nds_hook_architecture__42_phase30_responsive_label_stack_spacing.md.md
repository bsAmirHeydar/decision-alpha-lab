
---
type: source_card
source_path: "docs/nds_hook_architecture/42_phase30_responsive_label_stack_spacing.md"
source_ext: ".md"
source_size: 1487
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook", "Rally", "Zone / RTV"]
entities: []
---

# Source Card — 42_phase30_responsive_label_stack_spacing.md

## Source

[[docs/nds_hook_architecture/42_phase30_responsive_label_stack_spacing|docs/nds_hook_architecture/42_phase30_responsive_label_stack_spacing.md]]

## Summary

Fixed label offsets and fixed stack-step distances become visually wrong across timeframes: on smaller timeframes they can be too wide; on larger timeframes they can be too tight; crowded Hook zones need spacing that adapts to the local candle scale. Make Hook/branch label stacking responsive instead of relying on one dry absolute number. The label renderer now estimates the average candle range around the anchor node using a configurable local lookback window. From that local range it derives: base offset distance from the node; per-stack vertical step distance. Responsive values are clamped between configurable minima and maxima so spacing does not become absurdly tiny or huge. The existing fixed-point settings still exist, but now they act as floor values. If the responsive estimate is larger, the renderer uses the larger value. `responsive_label_offsets` `responsive_label_lookback_ba

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Phase 30 — Responsive Label Stack Spacing
  - Problem
  - Goal
  - What changed
    - 1) Dynamic spacing from local candle range
    - 2) Clamp bounds
    - 3) Manual values remain floors
  - New config knobs
  - Result

## Related Source Documents

- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `11`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `11`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/debug/E0007/README|README.md]] — score `10`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `10`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
