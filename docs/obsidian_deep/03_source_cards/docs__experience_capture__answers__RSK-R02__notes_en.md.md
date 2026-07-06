
---
type: source_card
source_path: "docs/experience_capture/answers/RSK-R02/notes_en.md"
source_ext: ".md"
source_size: 4864
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Execution / Risk", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/RSK-R02/notes_en|docs/experience_capture/answers/RSK-R02/notes_en.md]]

## Summary

This answer should be treated as: Risk sizing and convexity evaluation must be linked. Recommended flow: The system should not evaluate optionality only at entry. The system should not treat the input risk percent as true risk unless stop distance and commission confirm it. What is the default base account risk percent? What range should the setup-quality coefficient have? Should the coefficient be capped by risk policy? Should commission be included as round-trip or entry-side only? Should spread and slippage be mandatory in the first true-cost model? How should broker constraints alter the matched true cost? What happens if exact matching is impossible due to lot step? Is reward above 10R a hard target or a preferred class? What minimum potential reward makes a setup convex? How should context optionality be scored? How should zone optionality be scored? How should entry optionality be

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- RSK-R02 — Notes and Open Questions
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
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R03/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
