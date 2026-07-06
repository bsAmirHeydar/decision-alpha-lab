
---
type: source_card
source_path: "docs/experience_capture/answers/NDS-R03/question_en.md"
source_ext: ".md"
source_size: 1153
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Hook", "Rally", "UI / React"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/NDS-R03/question_en|docs/experience_capture/answers/NDS-R03/question_en.md]]

## Summary

Define node identity, node roles, node clustering, and node replacement in NDS. Nodes can start CycleHooks, act as Extreme anchors, appear inside sequences, appear in different Hook/Rally contexts, and change practical validity depending on role. The system needs a stable node identity model. Please clarify: When does a node remain the same node? When does a node become consumed, invalidated, replaced, merged, or archived? If several nodes are near each other, are they separate nodes or a cluster? Does changing L create a new node identity or a different view of the same market area? How do node roles differ: origin, anchor, destination, internal, Extreme anchor, sequence node? If one node appears in multiple sequences, does it keep the same node ID? How should node identity behave across fractal scales? Which nodes must be drawn on chart?

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- NDS-R03 — Node Identity, Node Cluster, and Node Replacement
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/NDS-R03|NDS-R03.md]] — score `12`
- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `10`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `8`
- [[docs/ai_execution/README|README.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
