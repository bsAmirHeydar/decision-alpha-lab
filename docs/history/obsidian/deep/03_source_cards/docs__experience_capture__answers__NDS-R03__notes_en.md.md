
---
type: source_card
source_path: "docs/experience_capture/answers/NDS-R03/notes_en.md"
source_ext: ".md"
source_size: 4146
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/NDS-R03/notes_en|docs/experience_capture/answers/NDS-R03/notes_en.md]]

## Summary

This answer should be treated as: The system should not store node meaning directly inside the node object. It should store: This keeps the core object strict while allowing rich context-dependent meanings. What exact rule creates the initial node_id? Should node_id include symbol, scale, time, price, and L? Should node identity be based on exact price/time or detected pivot object? If L changes and a node disappears, should it be marked absent in L-view or superseded? What exact rule defines node cluster width? Should clusters be based only on price distance, never time distance? Should cluster width depend on spread, cycle size, or symmetry? Should an invalidated origin node remain usable as a historical destination reference? Can a node lose one role and gain another later? Can a node be active in child scale and historical-only in parent scale? Should sequence membership allow one no

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- NDS-R03 — Notes and Open Questions
  - Classification
  - Core Hard Rules
  - Proposed Objects
  - Proposed Datasets
  - Proposed Fields
    - Node
    - NodeRole
    - NodeCluster
    - NodeSequenceMembership
    - FractalNodeRelation
  - Proposed Labels

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `22`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `16`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `16`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `16`
- [[docs/experience_capture/answers/DST-R03/notes_en|notes_en.md]] — score `16`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `16`
- [[docs/experience_capture/answers/EXT-04/notes_en|notes_en.md]] — score `16`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
