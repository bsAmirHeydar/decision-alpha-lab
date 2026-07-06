
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED.md"
source_ext: ".md"
source_size: 2455
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook", "UI / React"]
entities: []
---

# Source Card — ND_HOOK_BRANCHING_EXPLAINED.md

## Source

[[docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED|docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED.md]]

## Summary

Post-flag correction is not always a simple sequence: There can be multiple possible `1` nodes, and one later `2` can validate more than one earlier `1`. This is why hook logic cannot be a single linear counter. In a bullish post-flag correction, numbered nodes are lows. Imagine these lows appear: L1 can be a `1`. L2, being higher, can also be a new `1` in another branch. L3 passes below both L1 and L2. Therefore L3 can serve as `2` for both branches. L4 is higher again and can become a new `1` branch. The structure is not one counter. It is multiple hook branches. A practical way to count is from the latest adverse node backward. For bullish lows: Start from a current low. Move backward through previous lows. A prior higher low belongs to the same descending branch. If ordering breaks, create or switch branch. After branch construction, label from old to new. For bearish highs: Start fr

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- ND / Hook Branching Explained
  - Why Hook Counting Is Branchable
  - Bullish Example
  - End-Backward Counting
  - Why L Must Increase
  - ND Qualification
  - Why ND Can Overlap F
  - Why We Do Not Draw the 50% Line

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/ai_execution/README|README.md]] — score `10`
- [[docs/debug/E0007/README|README.md]] — score `10`
- [[docs/debug/E0008/README|README.md]] — score `10`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `10`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
