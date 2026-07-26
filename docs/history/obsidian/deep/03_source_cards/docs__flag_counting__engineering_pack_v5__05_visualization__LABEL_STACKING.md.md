
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/05_visualization/LABEL_STACKING.md"
source_ext: ".md"
source_size: 1801
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook"]
entities: []
---

# Source Card — LABEL_STACKING.md

## Source

[[docs/flag_counting/engineering_pack_v5/05_visualization/LABEL_STACKING|docs/flag_counting/engineering_pack_v5/05_visualization/LABEL_STACKING.md]]

## Summary

When all sequences are shown, label collision is unavoidable unless labels are stacked deterministically. Peak labels should be above peaks. Valley labels should be below valleys. This applies to F labels, internal numbers, ND labels, and origin markers when tied to a high/low node. Group labels by approximate chart location: Do not randomly offset each label. Near price to far from price: older sequence first; higher F-level first within same sequence age if needed; confirmed before candidate; ND/internal labels after owning F label unless specifically anchored to same node; deterministic id as final tie-breaker. The user preference is: For a high/peak anchor: For a low/valley anchor: Use ATR, chart scale, or fixed point distance. Recommended input: If labels become too far from price due to too many labels, do not randomize. Options: increase stack step compression; reduce font size; g

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Label Stacking
  - Purpose
  - Anchor Rule
  - Stack Buckets
  - Order Within Stack
  - Peak Placement
  - Valley Placement
  - Vertical Step
  - Avoid Huge Distance
  - Label Identity

## Related Source Documents

- [[docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS|OBJECT_NAMING_AND_LAYERS.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `8`
- [[docs/ai_execution/README|README.md]] — score `8`
- [[docs/debug/E0007/README|README.md]] — score `8`
- [[docs/debug/E0008/README|README.md]] — score `8`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `8`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
