
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa.md"
source_ext: ".md"
source_size: 1336
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa.md]]

## Summary

چرا مهم است: چون سیستم نباید مستقیم order بفرستد. NDS باید فقط ExecutionIntent بسازد و validator تصمیم بگیرد که قابل ارسال هست یا نه. پس قرارداد intent باید دقیق باشد. برای پاسخ، حتماً این موارد را روشن کن: • حداقل فیلدهای اجباری ExecutionIntent چیست؟ • scenario_id، zone_id، entry_extreme_id، node_id و destination_id چطور به هم وصل می‌شوند؟ • Structural price و adjusted price جدا ذخیره شوند؟ • Spread adjustment کجا ثبت شود؟ • Stop buffer و دلیلش کجا ثبت شود؟ • Risk budget و volume چطور ثبت شود؟ • Split orders داخل همان intent باشند یا child intents؟ • Cancel/replace/missed conditions داخل intent باشند؟ • Intent بدون broker validation قابل اجرا نیست؟ • چه چیزی intent را unsafe می‌کند؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • execution_intent_contract_v1.csv • execution_intent_lineage_v1.csv • structural_vs_adjusted_price_model_v1.csv • intent_safety_flags_v1.csv

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXE-R01 — ExecutionIntent Contract Finalization

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|question_en.md]] — score `11`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/architecture|architecture.md]] — score `10`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `10`
- [[docs/experience_capture/answers/DST-R03/notes_en|notes_en.md]] — score `10`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `10`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
