
---
type: source_card
source_path: "docs/experience_capture/answers/EXE-R01/notes_en.md"
source_ext: ".md"
source_size: 3643
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Execution / Risk", "Market Anatomy", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/EXE-R01/notes_en|docs/experience_capture/answers/EXE-R01/notes_en.md]]

## Summary

This answer should be treated as: ExecutionIntent should not be designed from broker fields first. It should be designed from NDS lineage first. Recommended flow: This keeps execution tied to NDS anatomy and prevents raw order-first design. What exact fields must be mandatory in ExecutionIntent? Which fields belong to NDS and which belong to broker validation? How should structural price and adjusted price be represented? How should spread adjustment be stored? How should stop buffer be stored? Should risk budget be part of the intent or attached by validator? Should volume be in the intent or computed later? Should split orders be child intents or child orders? Should cancel, replace, and missed rules be inside the intent or linked by policy IDs? What exact condition makes an intent unsafe? Should the first implementation be an `ExecutionIntentCandidate` only? Should all incomplete fiel

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXE-R01 — Notes and Open Questions
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

- [[docs/architecture|architecture.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `18`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `16`
- [[docs/flag_counting/README|README.md]] — score `16`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/DATA-R03/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
