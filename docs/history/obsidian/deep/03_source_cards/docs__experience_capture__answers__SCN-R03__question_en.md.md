
---
type: source_card
source_path: "docs/experience_capture/answers/SCN-R03/question_en.md"
source_ext: ".md"
source_size: 1239
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/SCN-R03/question_en|docs/experience_capture/answers/SCN-R03/question_en.md]]

## Summary

When several scenarios, contexts, or zones are alive at the same time, how should the system rank, keep, reject, or plan them together? NDS allows multiple interpretations, multiple zones, multiple destinations, multiple entry points, and different risk allocations. The system needs a policy for scenario ranking without forcing one scenario to become the… Please clarify: If both bullish and bearish scenarios exist, should both remain alive? Should several zones remain on the watchlist or should only one be selected? What makes a scenario or zone better? What creates a veto? Can several zones be planned with different risk? How should risk be split across scenarios? What if price reaches a weaker zone before a stronger zone? Can conditional long and short plans coexist? How should ranking update as market movement changes? What should the final algorithmic output be?

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- SCN-R03 — Scenario Ranking and Multi-Zone Selection
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/SCN-R03|SCN-R03.md]] — score `12`
- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `10`
- [[docs/experience_capture/answers/SCN-R03/answer_normalized_en|answer_normalized_en.md]] — score `9`
- [[docs/experience_capture/answers/SCN-R03/notes_en|notes_en.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
