
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_en.md"
source_ext: ".md"
source_size: 1110
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook", "Python Brain", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_en|docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_en.md]]

## Summary

چون اگر eventها و labelها دقیق ذخیره نشوند، بعداً train/test ممکن نیست. AI باید بداند چه چیزی ساخته، بسته، باطل، missed، fill یا completed شده است. چه زمانی node_created ثبت شود؟ CycleHook born/dead چطور ثبت شود؟ Sequence closed و X/Y closed چطور label شوند؟ Zone promoted و zone destroyed چطور ثبت شوند؟ Scenario born/updated/repriced/dead چطور ثبت شوند؟ Entry extreme created/invalidated چطور ثبت شود؟ Limit created/canceled/missed/replaced/filled چطور ثبت شود؟ Destination consumed/completed چطور ثبت شود؟ Position partially exited/fully exited چطور ثبت شود؟ Outcome metrics هر event چه باشد؟ خیر. پاسخ متنی کافی است. `nds_event_ledger_v1.csv` `training_label_taxonomy_v1.csv` `scenario_outcome_ledger_v1.csv` `entry_outcome_ledger_v1.csv`

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- DATA-R02 — Label and Event Ledger
  - Purpose
  - Required Clarifications
  - Image Requirement
  - Expected Derived Outputs

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/DST-R03/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-04/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R01/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R02/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
