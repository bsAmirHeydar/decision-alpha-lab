
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa.md"
source_ext: ".md"
source_size: 2427
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Python Brain", "Zone / RTV"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa.md]]

## Summary

چرا مهم است: چون بعد از ساختن Limit Entry، هنوز معلوم نیست سفارش تا چه زمانی زنده است، چه زمانی باید کنسل شود، چه زمانی missed حساب شود، و چه زمانی با یک Entry-Level Extreme جدید جایگزین شود. این بخش جلوی اجرای کور و سفا… برای پاسخ، حتماً این موارد را روشن کن: • وقتی parent zone سالم است ولی قیمت هنوز به limit نرسیده، سفارش تا چه زمانی زنده می‌ماند؟ • اگر سناریو، زون، یا محدودیت اصلی‌ای که سفارش را ساخته invalid شد، آیا pending limit فوراً cancel می‌شود؟ • اگر نود یا death boundary تایم ورود قبل از fill زده شد، سفارش چه وضعیتی می‌گیرد؟ • اگر قیمت بدون fill از زون برگشت و حرکت کرد، این missed است یا باید دنبال replace بگردیم؟ • Missed دقیقاً یعنی چه: حرکت به سمت مقصد بدون fill، خروج از زون، یا بسته‌شدن entry window؟ • Replace دقیقاً چه زمانی مجاز است؟ فقط وقتی Entry-Level Extreme جدید داخل همان زون ساخته شود یا در سناریوی هم‌خانواده هم مجاز است؟ • Entry جدید باید از قبلی بهتر باشد؟ مثلاً

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R03|ENT-R03.md]] — score `10`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_en|question_en.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `8`
- [[docs/experience_capture/answers/DST-R01/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
