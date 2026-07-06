
---
type: source_card
source_path: "docs/experience_capture/answers/NDS-R01/notes_en.md"
source_ext: ".md"
source_size: 3656
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Python Brain", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/NDS-R01/notes_en|docs/experience_capture/answers/NDS-R01/notes_en.md]]

## Summary

This answer should be treated as: The system should not feed AI raw candle data as the primary representation. The system should first construct NDS-native objects: AI should operate on this packet. Should X-axis and Y-axis be stored as separate tables or inside one state packet? What exact numeric rule defines Hook 1/2/3 symmetry? What exact numeric rule defines Hook 4 extension beyond symmetry? Should F2 >= F1 be measured by price distance, time, or both? Should F symmetry include both size and duration? How should parent timeframe dominance be scored when parent and child conflict? Should lower timeframe ever veto higher timeframe, or only refine entry? How should scale IDs be generated across symbols and timeframes? Should every Hook, Rally, Node, and F object be drawn on chart? Should symmetry be a hard requirement for some entries or only a scoring feature? Can symmetry define a zo

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- NDS-R01 — Notes and Open Questions
  - Classification
  - Core Hard Rules
  - Proposed Canonical Objects
  - Proposed Datasets
  - Proposed Fields for `canonical_state_packet_v1`
  - Proposed Labels
  - Proposed AI Modules
  - Architecture Consequence
  - Open Questions
  - Attachment Index

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `22`
- [[docs/experience_capture/questions/remaining_v2/by_code/NDS-R01|NDS-R01.md]] — score `22`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `20`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `20`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `20`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `20`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `19`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
