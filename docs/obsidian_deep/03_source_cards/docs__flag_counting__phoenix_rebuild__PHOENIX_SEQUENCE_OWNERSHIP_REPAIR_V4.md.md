
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4.md"
source_ext: ".md"
source_size: 3078
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4.md

## Source

[[docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4|docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4.md]]

## Summary

The previous Phoenix repairs improved individual components, but they still left the main chart as a candidate enumeration layer. Hook/ND roots, raw fail-open roots, and multiple L-scales could all emit independent F1 r… Within one active directional phase, a later same-direction F1 is not allowed to become a new main-chart chain merely because a local Hook/ND or a lower-L body exists. The active chain is still doing work. The engine was doing the following: Build Hook-derived roots. Optionally build fail-open roots. Build F1/F2/F3 chains from every root. Try to clean the chart with duplicate-body canonicalization. That is not a true state machine. Duplicate cleanup only removes nearly identical bodies. It cannot decide ownership when two F1 roots are different geometrically but belong to the same active directional phase. The main chart must be a sequence-state view, not a sliding-windo

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Sequence Ownership Repair V4
  - Failure that this patch addresses
  - Root cause
  - Correct contract
  - Implemented repair
  - Label discipline
  - What this patch does not change

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `16`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `16`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
