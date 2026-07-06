
---
type: source_card
source_path: "docs/experience_capture/answers/NDS-R03/answer_normalized_en.md"
source_ext: ".md"
source_size: 6778
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Rally", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/NDS-R03/answer_normalized_en|docs/experience_capture/answers/NDS-R03/answer_normalized_en.md]]

## Summary

Nodes are stable NDS objects. They do not lose their identity simply because their role changes. A node exists as a node, and then receives different roles depending on its placement inside Hook, Rally, CycleHook, sequence, Extreme, destination, invalidation, context, and scale. Therefore: Every detected NDS node should receive a stable identity. The node itself should not be redefined as a different object merely because it appears in different structures. A node can participate in multiple structures: The same node may hold several roles at the same time. A node's meaning comes from where it sits inside Hook and Rally definitions. The same node can have different significance depending on: This means the node table should separate identity from role. Suggested separation: The user explicitly states that there is no tolerance or leniency. This should be interpreted as: If a rule says a

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- NDS-R03 — Normalized Interpretation
  - Core Claim
  - Node Identity Rule
  - Node Role Is Contextual
  - No Leniency / No Approximate Identity
  - Identity vs Validity
  - Node Role Taxonomy
  - Role-Specific Validity
  - Node Consumption
  - Node Replacement
  - Node Cluster
  - Node in Multiple Sequences

## Related Source Documents

- [[docs/experience_capture/questions/by_code/EXT-06|EXT-06.md]] — score `16`
- [[docs/experience_capture/questions/by_code/EXT-07|EXT-07.md]] — score `16`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `14`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
