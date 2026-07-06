
---
type: source_card
source_path: "docs/experience_capture/answers/EXE-R01/answer_normalized_en.md"
source_ext: ".md"
source_size: 4876
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Hook", "Market Anatomy", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/EXE-R01/answer_normalized_en|docs/experience_capture/answers/EXE-R01/answer_normalized_en.md]]

## Summary

The detailed field-level contract for ExecutionIntent is not fully known yet. However, the upstream decision logic is known: ExecutionIntent should therefore not be treated as a raw order request. It is the final structured expression of a fractal NDS decision pipeline. The user explicitly states that the detailed fields are not known. This must be preserved honestly. The following should remain open: These should not be over-specified prematurely. The known part is architectural. The system begins from the four-state view established in BASE records: This view is not read once at a single timeframe. It is read fractally. The four-state view becomes decision structure across: Then trade decisions are made based on the quality of those layers. The four-state view should be evaluated across scales. Suggested interpretation: This is not necessarily a fixed timeframe mapping. It is a fractal

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXE-R01 — Normalized Interpretation
  - Core Claim
  - Unknown Field-Level Contract
  - Known Decision Pipeline
  - Fractal Four-State View
  - Context, Zone, Entry Conversion
  - Quality-Based Trade Decision
  - ExecutionIntent as Candidate, Not Order
  - Minimum Known Contract
  - Intent Creation Logic
  - Machine-Readable Summary
  - Short Formal Statement

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/SCN-R02|SCN-R02.md]] — score `18`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/NDS-R01/question_en|question_en.md]] — score `16`
- [[docs/experience_capture/questions/remaining_v2/by_code/NDS-R01|NDS-R01.md]] — score `16`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY|README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY.md]] — score `16`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_REVERSE_EXTREME_FRACTAL_ENTRY_PHILOSOPHY|README_FLAG_REVERSE_EXTREME_FRACTAL_ENTRY_PHILOSOPHY.md]] — score `16`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
