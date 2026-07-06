
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM.md"
source_ext: ".md"
source_size: 1783
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — NODE_ENGINE_ALGORITHM.md

## Source

[[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM.md]]

## Summary

Use existing project node logic. Flag Counting should call it as a dependency. Recommended adapter: Node fields: For candidate high plateau at price P: Merge equal highs into one candidate. Do not count equal adjacent highs as clearance. Require at least L candles left with high < P. Require at least L candles right with high < P. Emit high node. For candidate low plateau at price P: Merge equal lows into one candidate. Do not count equal adjacent lows as clearance. Require at least L candles left with low > P. Require at least L candles right with low > P. Emit low node. Nodes should be sorted by: The engine may request several L values. Example: Hook readability may increase L dynamically. Do not delete old nodes because later price passed them. Historical nodes remain part of identity and audit. Use helper functions: Default: Equality returns false. Minimum tests: Equal high plateau b

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Node Engine Algorithm
  - Source
  - Required Interface
  - Extraction Semantics
  - Ordering
  - Multi-L Views
  - No Expiration
  - Break Function
  - Adapter Tests

## Related Source Documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|MODULE_ARCHITECTURE.md]] — score `13`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|README.md]] — score `13`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|answer_normalized_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
