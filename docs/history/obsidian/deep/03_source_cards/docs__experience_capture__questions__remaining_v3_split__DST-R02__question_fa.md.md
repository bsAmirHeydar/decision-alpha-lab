
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa.md"
source_ext: ".md"
source_size: 1600
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Python Brain"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa|docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa.md]]

## Summary

چرا مهم است: چون در مدل تو سود فقط یک TP ثابت نیست؛ ممکن است چند مقصد، خروج پله‌ای، runner و tail داشته باشیم. این سیاست باید از سناریو و position جدا ولی متصل تعریف شود. برای پاسخ، حتماً این موارد را روشن کن: • TP اولیه کجا قرار می‌گیرد؟ • TP همیشه روی مقصد است یا کمی قبل/بعد از مقصد؟ • خروج پله‌ای چند مرحله‌ای چطور تصمیم‌گیری می‌شود؟ • چند درصد در مقصد اول، دوم، سوم بسته می‌شود؟ • خروج پله‌ای rule-based است یا trainable؟ • اگر مقصد اول نزدیک باشد ولی مقصد دوم خیلی باز باشد، چطور تصمیم می‌گیریم؟ • آیا می‌شود بخشی از معامله را برای tail / explosion باز گذاشت؟ • بعد از خروج اول، stop بقیه position چه می‌شود؟ • Break-even مجاز است یا با منطق convexity تضاد دارد؟ • خروج نهایی چه زمانی است؟ عکس لازم: اختیاری. اگر نمونه چند مقصد و خروج پله‌ای داری، عکس کمک می‌کند. خروجی مورد انتظار بعد از پاسخ: • take_profit_policy_v1.csv • partial_exit_policy_v1.csv • multi_destination_exit_model_v1.csv • ru

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

## Entities

—

## Headings

- DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_en|question_en.md]] — score `7`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `6`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `6`
- [[docs/experience_capture/answers/DST-R01/notes_en|notes_en.md]] — score `6`
- [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] — score `6`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `6`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `6`
- [[docs/experience_capture/answers/ENT-R03/notes_en|notes_en.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
