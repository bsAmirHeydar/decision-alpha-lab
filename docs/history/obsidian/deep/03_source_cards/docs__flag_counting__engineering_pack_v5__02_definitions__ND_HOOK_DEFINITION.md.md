
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION.md"
source_ext: ".md"
source_size: 2947
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React"]
entities: []
---

# Source Card — ND_HOOK_DEFINITION.md

## Source

[[docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION|docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION.md]]

## Summary

ND and Hook are one phase family in this contract. They describe multi-node correction/cycle behavior using high/low nodes only. ND/Hook is not based on candle close. ND/Hook can appear: after a flag body as post-flag correction; inside a larger active sequence; as a phase before F1; in overlapping contexts if separate logical contexts emit them. All ND/Hook structures are displayed by default. An input may restrict display to open sequence contexts: ND/Hook numbering uses adverse-side nodes. Bullish context: Bearish context: Two numbered adverse-side nodes are internal 1/2 only. They are not ND. Three or four numbered adverse-side nodes form ND/Hook if other requirements pass. These should receive both number labels and ND/Hook label. More than four numbered nodes are not allowed in final readable view. If any hook branch has more than four numbered nodes, increase L and rebuild the vie

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- ND / Hook Definition
  - General Definition
  - Scope
  - Numbered Nodes
  - Two Nodes
  - Three or Four Nodes
  - More Than Four Nodes
  - Branching
  - ND 50% Cycle Rule
  - ND Rendering
  - ND and F Overlap

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/ai_execution/README|README.md]] — score `12`
- [[docs/debug/E0008/README|README.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
