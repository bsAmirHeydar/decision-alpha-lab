
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/DST-R02/question_en.md"
source_ext: ".md"
source_size: 1486
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Python Brain", "UI / React"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_en|docs/experience_capture/questions/remaining_v3_split/DST-R02/question_en.md]]

## Summary

چون در مدل تو سود فقط یک TP ثابت نیست؛ ممکن است چند مقصد، خروج پله‌ای، runner و tail داشته باشیم. این سیاست باید از سناریو و position جدا ولی متصل تعریف شود. TP اولیه کجا قرار می‌گیرد؟ TP همیشه روی مقصد است یا کمی قبل/بعد از مقصد؟ خروج پله‌ای چند مرحله‌ای چطور تصمیم‌گیری می‌شود؟ چند درصد در مقصد اول، دوم، سوم بسته می‌شود؟ خروج پله‌ای rule-based است یا trainable؟ اگر مقصد اول نزدیک باشد ولی مقصد دوم خیلی باز باشد، چطور تصمیم می‌گیریم؟ آیا می‌شود بخشی از معامله را برای tail / explosion باز گذاشت؟ بعد از خروج اول، stop بقیه position چه می‌شود؟ Break-even مجاز است یا با منطق convexity تضاد دارد؟ خروج نهایی چه زمانی است؟ اختیاری. اگر نمونه چند مقصد و خروج پله‌ای داری، عکس کمک می‌کند. `take_profit_policy_v1.csv` `partial_exit_policy_v1.csv` `multi_destination_exit_model_v1.csv` `runner_tail_position_policy_v1.csv`

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy
  - Purpose
  - Required Clarifications
  - Image Requirement
  - Expected Derived Outputs

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `8`
- [[docs/experience_capture/answers/DST-R01/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/ENT-R02/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/ENT-R03/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/EXE-R01/notes_en|notes_en.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
