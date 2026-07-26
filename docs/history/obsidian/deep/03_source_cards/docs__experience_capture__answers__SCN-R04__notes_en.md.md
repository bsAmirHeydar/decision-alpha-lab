
---
type: source_card
source_path: "docs/experience_capture/answers/SCN-R04/notes_en.md"
source_ext: ".md"
source_size: 4447
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Execution / Risk", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/SCN-R04/notes_en|docs/experience_capture/answers/SCN-R04/notes_en.md]]

## Summary

This answer should be treated as: The scenario engine should not recompute scenarios as anonymous fresh objects every time. It should preserve scenario identity and update its state. Recommended update flow: This creates an auditable scenario lifecycle. Which constraints are core constraints versus secondary constraints? What minimum constraint integrity score keeps a scenario alive? How should partial constraint weakening be measured? What exact condition triggers repricing? Can a repriced scenario remain the same scenario if its zone changes completely? How should relative weight be normalized across opposite directions? How should weight update interact with risk budget? Can a vetoed scenario return to tradable state? Can a dead scenario be reborn, or does it create a new scenario_id? What state transition happens after actual trade entry? Should filled scenarios continue in the scena

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- SCN-R04 — Notes and Open Questions
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
- [[docs/experience_capture/questions/remaining_v2/by_code/SCN-R04|SCN-R04.md]] — score `16`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
