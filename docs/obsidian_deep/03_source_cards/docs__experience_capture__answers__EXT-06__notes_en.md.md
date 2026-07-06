
---
type: source_card
source_path: "docs/experience_capture/answers/EXT-06/notes_en.md"
source_ext: ".md"
source_size: 3272
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/EXT-06/notes_en|docs/experience_capture/answers/EXT-06/notes_en.md]]

## Summary

This experience should be treated as: This rule should live in a deterministic gate before AI policy. Suggested gate: Possible outputs: Does "one point beyond the node" refer to bid/ask, mid, candle wick, or chart price? For buy entries, should penetration be evaluated using bid or ask? For sell entries, should penetration be evaluated using bid or ask? Should the system store raw chart penetration separately from executable broker stop penetration? Does spread affect structural penetration or only execution stop placement? Can a new Extreme be created immediately after penetration if a new NDS structure forms? Should penetration-then-reversal be used to widen future Extreme zones, or only to analyze stop fragility? Should the old scenario die when the Extreme anchor dies, or only the entry candidate? If parent scenario remains alive but lower Extreme dies, should the system look for a n

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXT-06 — Notes and Open Questions
  - Classification
  - Proposed Hard Rule
  - Proposed States
  - Proposed Datasets
  - Proposed Fields
  - Proposed Labels
  - Proposed AI Modules
  - Architecture Consequence
  - Open Questions
  - Attachment Index

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `22`
- [[docs/experience_capture/questions/by_code/EXT-06|EXT-06.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/DST-R03/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
