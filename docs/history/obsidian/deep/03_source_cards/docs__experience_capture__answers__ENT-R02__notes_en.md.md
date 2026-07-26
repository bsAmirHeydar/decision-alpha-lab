
---
type: source_card
source_path: "docs/experience_capture/answers/ENT-R02/notes_en.md"
source_ext: ".md"
source_size: 4175
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/ENT-R02/notes_en|docs/experience_capture/answers/ENT-R02/notes_en.md]]

## Summary

This answer should be treated as: ENT-R02 should not directly execute trades. It should create an `ExecutionIntent`. Recommended flow: This preserves the no-send architecture. Should the stop buffer be trained globally first or per symbol/timeframe? What candidate buffer values should be tested first? Should buffer be measured in points, spread multiples, or node-distance percentage? Can the buffer ever move the stop so far that the trade loses convexity? What is the maximum allowed buffer before entry is vetoed? Should buy limit stop and take profit also have any spread adjustment, or only entry? For sell limit, should entry price ever be spread-adjusted, or only stop loss and take profit as stated? Should max-lot split orders share the same SL/TP or allow staggered targets? If split orders are created, should they share one scenario ID and one entry_extreme_id? Should partial fills cre

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- ENT-R02 — Notes and Open Questions
  - Classification
  - Core Hard Rules
  - Core Learnable Policies
  - Proposed Objects
  - Proposed Datasets
  - Proposed Fields
  - Proposed Labels
  - Proposed AI Modules
  - Architecture Consequence
  - Open Questions
  - Attachment Index

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `22`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `16`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `16`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `16`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `16`
- [[docs/experience_capture/answers/ENT-R03/notes_en|notes_en.md]] — score `16`
- [[docs/experience_capture/answers/EXT-01/notes_en|notes_en.md]] — score `16`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
