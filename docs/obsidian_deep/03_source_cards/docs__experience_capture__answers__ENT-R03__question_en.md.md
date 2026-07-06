
---
type: source_card
source_path: "docs/experience_capture/answers/ENT-R03/question_en.md"
source_ext: ".md"
source_size: 1637
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/ENT-R03/question_en|docs/experience_capture/answers/ENT-R03/question_en.md]]

## Summary

After a Limit Entry is created from a valid Entry-Level Extreme, how long should the pending limit remain alive, when should it be canceled or deleted, and how should missed or replacement behavior be defined? ENT-R01 defined the Entry-Level Extreme as Extreme Near Death. ENT-R02 defined the practical entry geometry: limit entry, stop behind node, trainable buffer, spread adjustment, and max-lot splitting. ENT-R03 defines the lifecycle of the pending limit before fill. Please clarify: While the parent zone is alive but price has not reached the limit, how long does the pending order remain alive? If the scenario, zone, or original reason that created the order becomes invalid, should the pending order be canceled immediately? If the entry-scale node or death boundary is hit before fill, what happens? If price moves without filling the order, is it missed or should the system seek replace

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R01|ENT-R01.md]] — score `12`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R02|ENT-R02.md]] — score `12`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R03|ENT-R03.md]] — score `12`
- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `10`
- [[docs/experience_capture/answers/ENT-R03/notes_en|notes_en.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
