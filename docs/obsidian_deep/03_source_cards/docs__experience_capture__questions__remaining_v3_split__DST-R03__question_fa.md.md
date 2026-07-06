
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/DST-R03/question_fa.md"
source_ext: ".md"
source_size: 1608
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Python Brain"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/DST-R03/question_fa|docs/experience_capture/questions/remaining_v3_split/DST-R03/question_fa.md]]

## Summary

چرا مهم است: چون مقصدها با حرکت بازار ثابت نمی‌مانند. بعضی مصرف می‌شوند، بعضی repriced می‌شوند، بعضی وزن می‌گیرند یا می‌میرند. بدون lifecycle مقصد، optionality و position management ناقص می‌ماند. برای پاسخ، حتماً این موارد را روشن کن: • مقصد چه زمانی consumed می‌شود؟ • تاچ مقصد کافی است یا باید قیمت از آن عبور کند؟ • اگر مقصد اول خورده شد، مقصدهای بعدی چگونه وزن می‌گیرند؟ • اگر مقصد جدید ساخته شد، آیا به لیست مقصدها اضافه می‌شود؟ • اگر مقصد قبلی دیگر optionality ندارد، حذف می‌شود یا historical می‌ماند؟ • مقصدهای opposite direction با position فعال چه می‌کنند؟ • اگر مقصد نزدیک شود، position کاهش می‌یابد یا فقط optionality score پایین می‌آید؟ • مقصد با سناریو می‌میرد یا lifecycle مستقل دارد؟ • مقصدهای parent و child چطور به هم وصل می‌شوند؟ • خروجی state machine مقصد چیست؟ عکس لازم: اختیاری. خروجی مورد انتظار بعد از پاسخ: • destination_state_machine_v1.csv • destination_repricing_policy_v1.

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

## Entities

—

## Headings

- DST-R03 — Destination Repricing and Completion

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v3_split/DST-R03/question_en|question_en.md]] — score `5`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `4`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `4`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `4`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `4`
- [[docs/experience_capture/answers/DST-R01/notes_en|notes_en.md]] — score `4`
- [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] — score `4`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `4`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `4`
- [[docs/experience_capture/answers/ENT-R03/notes_en|notes_en.md]] — score `4`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
