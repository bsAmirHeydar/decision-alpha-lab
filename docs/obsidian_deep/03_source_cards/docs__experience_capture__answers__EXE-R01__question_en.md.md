
---
type: source_card
source_path: "docs/experience_capture/answers/EXE-R01/question_en.md"
source_ext: ".md"
source_size: 1278
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/EXE-R01/question_en|docs/experience_capture/answers/EXE-R01/question_en.md]]

## Summary

What should the ExecutionIntent contract contain, and how should NDS convert structural analysis into a safe executable intent without sending broker orders directly? Previous records established that NDS should not directly send orders. It should produce a structured ExecutionIntent that is later validated by broker and safety layers. However, the exact field-level contract is not fu… Please clarify: What is known about the structure behind ExecutionIntent? Should the four-state view be read fractally? How does the four-state view become context, zone, and entry? Should decisions be made based on quality at those levels? Which parts of the ExecutionIntent contract are still unknown? What should remain trainable? What should the final output model contain?

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXE-R01 — ExecutionIntent Contract Finalization
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/EXE-R01|EXE-R01.md]] — score `12`
- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `10`
- [[docs/experience_capture/answers/EXE-R01/answer_normalized_en|answer_normalized_en.md]] — score `7`
- [[docs/experience_capture/answers/EXE-R01/notes_en|notes_en.md]] — score `7`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
