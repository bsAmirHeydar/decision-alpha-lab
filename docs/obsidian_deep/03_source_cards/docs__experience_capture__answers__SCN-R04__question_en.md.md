
---
type: source_card
source_path: "docs/experience_capture/answers/SCN-R04/question_en.md"
source_ext: ".md"
source_size: 1116
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/SCN-R04/question_en|docs/experience_capture/answers/SCN-R04/question_en.md]]

## Summary

When market movement changes, when should a scenario remain alive, be updated, be repriced, move to watchlist, be vetoed, or die? NDS allows multiple live scenarios and zones. Ranking is dynamic. A scenario is not necessarily a truth claim; it is a convex opportunity thread based on constraints. The system needs a state model for scenario updates. Please clarify: What keeps a scenario alive? What changes scenario rank? When is a scenario repriced instead of killed? What kills a scenario? What is the difference between veto and death? When does a scenario move to watchlist? What happens if price moves without entry? What happens after entry? How do destinations affect scenario continuation? What scenario states should exist?

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- SCN-R04 — Scenario Update, Death, and Repricing
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/SCN-R04|SCN-R04.md]] — score `14`
- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `10`
- [[docs/experience_capture/answers/SCN-R04/answer_normalized_en|answer_normalized_en.md]] — score `9`
- [[docs/experience_capture/answers/SCN-R04/notes_en|notes_en.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
