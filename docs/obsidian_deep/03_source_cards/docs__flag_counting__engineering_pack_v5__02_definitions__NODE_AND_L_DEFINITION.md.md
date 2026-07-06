
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/02_definitions/NODE_AND_L_DEFINITION.md"
source_ext: ".md"
source_size: 3288
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Flag Counting", "UI / React"]
entities: []
---

# Source Card — NODE_AND_L_DEFINITION.md

## Source

[[docs/flag_counting/engineering_pack_v5/02_definitions/NODE_AND_L_DEFINITION|docs/flag_counting/engineering_pack_v5/02_definitions/NODE_AND_L_DEFINITION.md]]

## Summary

The Flag Counting engine must reuse the existing project node module. Do not rewrite node logic locally inside Flag Counting unless the local implementation is a byte-for-byte or behavior-identical adapter of the project node logic. The structural inputs are: The following are not structural inputs: L is the minimum clearance count on both sides of a candidate high/low price. For a High node candidate at price `P`: For a Low node candidate at price `P`: Equality is special and must follow existing project plateau handling. Equal highs/lows are treated as one plateau-style node. High plateau: Low plateau: Important: equal-price bars inside or beside the plateau do not count as extra clearance; equality does not create multiple separate nodes; equality does not count as a break; the node must still receive at least L real non-reaching candles on each side. A confirmed node does not expire.

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Node and L Definition
  - Source of Truth
  - Raw Inputs
  - L Definition
  - Equal Highs and Equal Lows
  - Node Stability
  - Node Identity
  - Strict Pass Logic
  - Tolerance
  - Node Views
  - Implementation Warning

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/debug/E0008/README|README.md]] — score `8`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/EXT-02/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/SCN-R02/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
