
---
type: source_card
source_path: "docs/experience_capture/answers/ENT-R04/question_en.md"
source_ext: ".md"
source_size: 1764
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/ENT-R04/question_en|docs/experience_capture/answers/ENT-R04/question_en.md]]

## Summary

After a Limit Entry is filled, how should the system transition from Scenario / ExecutionIntent into an active Position? Should the scenario remain alive, should it become a PositionThread, how should duplicate entries b… ENT-R01 defined Entry-Level Extreme as Extreme Near Death. ENT-R02 defined limit entry, stop geometry, spread adjustment, trainable buffer, and max-lot splitting. ENT-R03 defined pending limit lifecycle as reason-integrity based. ENT-R04 defines what happens after fill. Please clarify: After fill, does the ScenarioThread remain alive or become a PositionThread? Should the system prevent duplicate trades with the same reasons while the position is open? If the parent scenario weakens after entry, what happens to the position? If an opposite scenario becomes stronger after entry, should the system reduce, hedge, or only manage stop/TP? Can stops move after fill? Can exits

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- ENT-R04 — After Fill: Scenario-to-Position Transition
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R01|ENT-R01.md]] — score `12`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R02|ENT-R02.md]] — score `12`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R03|ENT-R03.md]] — score `12`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R04|ENT-R04.md]] — score `12`
- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `10`
- [[docs/experience_capture/answers/ENT-R04/answer_normalized_en|answer_normalized_en.md]] — score `7`
- [[docs/experience_capture/answers/ENT-R04/notes_en|notes_en.md]] — score `7`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
