
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3.md"
source_ext: ".md"
source_size: 2513
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3.md

## Source

[[docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3|docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3.md]]

## Summary

This repair re-separates the Phoenix engine into three hard layers: **Structure layer**: F1/F2/F3 two-leg flag bodies are the primary chart structures. **Context layer**: Hook/ND is a phase-boundary/context source. It must never erase valid flag structures. **Presentation layer**: the main chart renders canonical visible structures only; audit labels remain optional. Hook/ND cannot be the only source of F roots. Hook-derived roots are built first, but raw-origin fail-open roots are also inspected when fail-open is enabled. Duplicate visual bodies are hidden after detection, not before the engine has a chance to recover valid F structures. F2 can only be emitted from a confirmed F1. F3 can only be emitted from a confirmed F2. A body smaller than the F2/F1 size contract is not a main-chart F2 and cannot parent F3. A hidden root hides its descendants, so orphan F2/F3 objects cannot remain o

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Main-Chart Contract Repair V3
  - Red lines enforced
  - Main chart defaults
  - Audit mode
  - Canonicalization

## Related Source Documents

- [[docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4|PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4.md]] — score `15`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
