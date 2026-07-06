
---
type: source_card
source_path: "docs/experience_capture/answers/DST-R02/notes_en.md"
source_ext: ".md"
source_size: 4033
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Execution / Risk", "Path Smoothness", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/DST-R02/notes_en|docs/experience_capture/answers/DST-R02/notes_en.md]]

## Summary

This answer should be treated as: DST-R02 should not hard-code one exit rule. Recommended flow: Trailing should be treated as a tested optional family, not the default. What exact NDS conditions should trigger partial close? Should partial close be based on destination, optionality decay, opposite scenario, or structure completion? How many partial exits should be allowed? What default partial percentages should be tested first? What minimum runner size should remain open? Can the runner be closed only by destination completion? Should break-even be considered a trailing-like behavior or a separate policy? What trailing variants should be tested as baselines? What result would make trailing acceptable despite skepticism? How should exit policy cost be calculated? Should exit policies be trained globally or per market/timeframe? Should partial exit performance be attributed to exit logic

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- DST-R02 — Notes and Open Questions
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
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `16`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
