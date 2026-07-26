
---
type: source_card
source_path: "docs/experience_capture/answers/EXT-08/answer_normalized_en.md"
source_ext: ".md"
source_size: 4248
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/EXT-08/answer_normalized_en|docs/experience_capture/answers/EXT-08/answer_normalized_en.md]]

## Summary

Node freshness is not a primary standalone decision rule. The system should not first ask: The system should first ask: Only after context and zone are defined should the system evaluate Extreme entries and their anchor nodes. The correct hierarchy is: This means freshness is secondary. A fresh node is not automatically valid. An old node is not automatically invalid. A node becomes relevant when it belongs to the correct NDS context and the correct trading region. The answer explicitly says: This means the system should not hardcode a rule such as: Freshness can be stored as a feature, but it should not become a blind rule. The system prioritizes reward and convexity over win rate. The project accepts that Extreme-style entries may have many stop-outs. This is acceptable because the risk is intended to be very small and the reward can be very large. Possible acceptable win-rate range fr

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXT-08 — Normalized Interpretation
  - Core Claim
  - Correct Decision Sequence
  - No Fresh-vs-Old Separation by Default
  - Reward-First Logic
  - Win Rate Is Secondary, Not Irrelevant
  - Node Expiry
  - Freshness as a Feature
  - What the System Should Test
  - AI Relevance
  - Short Formal Statement

## Related Source Documents

- [[docs/experience_capture/questions/by_code/EXT-06|EXT-06.md]] — score `16`
- [[docs/experience_capture/questions/by_code/EXT-08|EXT-08.md]] — score `16`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `11`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/debug/E0006/README|README.md]] — score `10`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `10`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
