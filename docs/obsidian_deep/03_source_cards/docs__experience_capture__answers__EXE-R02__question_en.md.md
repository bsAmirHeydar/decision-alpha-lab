
---
type: source_card
source_path: "docs/experience_capture/answers/EXE-R02/question_en.md"
source_ext: ".md"
source_size: 1225
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/EXE-R02/question_en|docs/experience_capture/answers/EXE-R02/question_en.md]]

## Summary

How should the broker validator and send gate treat broker constraints such as minimum stop distance, tick size, digits, lot step, min/max lot, margin, spread, freeze level, trade mode, market session, and order rejectio… NDS should not directly send orders. Previous records established that NDS produces an ExecutionIntent or ExecutionIntentCandidate, and broker/safety validation comes later. EXE-R02 defines the nature of the broker valid… Please clarify: Are broker constraints part of NDS ontology or mechanical validation? Are these rules clear and deterministic? Should the broker validator train anything about the market structure? Should the validator change the NDS reasoning? Should this layer merely approve, adjust mechanically, or veto? What should the final output model contain?

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- EXE-R02 — Broker Validator and Send Gate
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/EXE-R02|EXE-R02.md]] — score `12`
- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `10`
- [[docs/experience_capture/answers/EXE-R02/answer_normalized_en|answer_normalized_en.md]] — score `7`
- [[docs/experience_capture/answers/EXE-R02/notes_en|notes_en.md]] — score `7`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
