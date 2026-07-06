
---
type: source_card
source_path: "docs/experience_capture/answers/ENT-R02/question_en.md"
source_ext: ".md"
source_size: 1171
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Hook", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/ENT-R02/question_en|docs/experience_capture/answers/ENT-R02/question_en.md]]

## Summary

When a valid Entry-Level Extreme / Extreme Near Death exists inside a zone, how should limit entry, stop geometry, spread adjustment, buffer, fill policy, and order splitting be defined? ENT-R01 defined the entry-level Extreme as Extreme Near Death: an entry-scale CycleHook excessively close to death, used to reduce stop size and improve convexity. ENT-R02 defines the practical limit-order geometry and e… Please clarify: Where is the limit entry placed? Where is the stop placed? Is there a buffer behind the stop? Is the buffer fixed or trainable? How should spread be handled for buy limit and sell limit? Should broker constraints be part of NDS or execution validation? If max lot is hit, should the order be split? What should the output object contain?

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R02|ENT-R02.md]] — score `16`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R01|ENT-R01.md]] — score `14`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `12`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/ENT-R01/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `12`
- [[docs/experience_capture/answers/ENT-R01/question_en|question_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
