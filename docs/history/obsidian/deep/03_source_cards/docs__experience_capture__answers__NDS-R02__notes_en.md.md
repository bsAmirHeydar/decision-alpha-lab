
---
type: source_card
source_path: "docs/experience_capture/answers/NDS-R02/notes_en.md"
source_ext: ".md"
source_size: 5155
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook", "Python Brain", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/NDS-R02/notes_en|docs/experience_capture/answers/NDS-R02/notes_en.md]]

## Summary

This answer should be treated as: The first implementation should separate deterministic construction from learnable scoring. Deterministic construction: Learnable scoring: What exact node detector feeds the CycleHook builder at L2 and higher L values? Should a node that appears in multiple sequences have multiple sequence roles or one canonical role plus references? How should a sequence starter be defined when multiple nodes occur at nearly the same price? Should strict lower/higher comparison use raw price or normalized point/tick value? Should spread ever affect equality or strictness, or is sequence logic purely chart-price based? What exact retracement formula should be used for the 50% closure rule? Should retracement be measured by wick, close, or any price touch? What exact condition defines ND zone before origin penetration? Should ND be built from fixed-origin L view, recalcul

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- NDS-R02 — Notes and Open Questions
  - Classification
  - Core Hard Rules
  - Core Flexible / Learnable Policies
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
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/DST-R03/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-04/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
