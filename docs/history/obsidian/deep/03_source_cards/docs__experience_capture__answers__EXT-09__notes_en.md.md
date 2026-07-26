
---
type: source_card
source_path: "docs/experience_capture/answers/EXT-09/notes_en.md"
source_ext: ".md"
source_size: 4124
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Python Brain", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/EXT-09/notes_en|docs/experience_capture/answers/EXT-09/notes_en.md]]

## Summary

This experience should be treated as: The future system should not make `extreme_anchor_node_quality` the top-level decision source. Instead, the system should separate: Anchor quality is a secondary/refinement layer. Should `extreme_anchor_node_quality` be a score, class, or both? Which anchor-quality features are allowed in v1? Should prior touch count be stored even if it is not trusted yet? How should path cleanliness toward the node be measured in NDS terms? Can parent-zone proximity improve anchor quality without becoming the main reason? Can destination openness outweigh a weak anchor? What defines a weak node if anchor quality is secondary? Should anchor quality improve win rate only, or expected R? How much reward sacrifice is unacceptable when improving win rate? Should learned rules be written to Markdown automatically after every training run? Should every model branch have a

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXT-09 — Notes and Open Questions
  - Classification
  - Main Design Consequence
  - Proposed Hard Rules
  - Proposed Flexible Rules
  - Proposed Datasets
  - Proposed Fields
  - Proposed Labels
  - Proposed AI Modules
  - Proposed Research Workflow
  - Open Questions
  - Attachment Index

## Related Source Documents

- [[docs/experience_capture/questions/by_code/EXT-09|EXT-09.md]] — score `18`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `12`
- [[docs/architecture|architecture.md]] — score `12`
- [[docs/experience_capture/answers/DST-R03/notes_en|notes_en.md]] — score `12`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
