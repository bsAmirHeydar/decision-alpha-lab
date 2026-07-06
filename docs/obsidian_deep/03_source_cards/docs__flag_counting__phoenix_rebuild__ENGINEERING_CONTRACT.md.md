
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/ENGINEERING_CONTRACT.md"
source_ext: ".md"
source_size: 2479
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — ENGINEERING_CONTRACT.md

## Source

[[docs/flag_counting/phoenix_rebuild/ENGINEERING_CONTRACT|docs/flag_counting/phoenix_rebuild/ENGINEERING_CONTRACT.md]]

## Summary

A node is extracted from high/low data only. `L` is the number of candles on each side that must not reach the node price. Equal highs/lows are collapsed into one plateau node. The anchor time is the last equal touch of… Equality is never a break. For a bullish boundary, price must move strictly below the boundary to break it. For a bearish boundary, price must move strictly above the boundary to break it. A flag body is the invariant object: Bullish: Origin is a low node. Leg1 is the highest high before the correction. Waist is the deepest correction low after Leg1 that does not break Origin. Leg2 is the high that breaks Leg1. Bearish is symmetric. F1 is displayed after the two-leg body exists. F1 confirms only after a valid internal 1/2 or more forms after Leg2 and price then breaks Leg2 again before F1 Waist is broken. F1 invalidation before confirmation is the Waist. F2 is authorized

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Engineering Contract: Phoenix Flag Counting
  - Node contract
  - Flag body contract
  - F1 contract
  - F2 contract
  - F3 contract
  - Hook/ND contract
  - Renderer contract

## Related Source Documents

- [[docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES|IMPLEMENTATION_NOTES.md]] — score `11`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3|PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3.md]] — score `11`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2|PHOENIX_ROOT_CONTRACT_REPAIR_V2.md]] — score `11`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4|PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4.md]] — score `11`
- [[docs/flag_counting/phoenix_rebuild/README|README.md]] — score `11`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `10`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
