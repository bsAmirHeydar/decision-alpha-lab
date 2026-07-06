
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/AI-R03/question_en.md"
source_ext: ".md"
source_size: 1217
empty: false
generated_at: 2026-07-06
concepts: ["Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/AI-R03/question_en|docs/experience_capture/questions/remaining_v3_split/AI-R03/question_en.md]]

## Summary

چون قبلاً گفتی اگر AI خلاف تجربه تو نتیجه بهتر گرفت، باید شرایط قبولش مشخص باشد. باید فرق recommendation، auto-apply، branch test و core promotion روشن شود. وقتی AI خلاف تجربه تو نتیجه بهتر گرفت، کجا قابل قبول است؟ چه سطح شواهدی لازم است؟ کدام تغییرات فقط recommendation هستند؟ کدام تغییرات می‌توانند auto-apply شوند؟ Branch-by-branch test لازم است؟ آیا چند الگوریتم باید یک نتیجه را تأیید کنند؟ چه چیزهایی باید در گزارش انسانی بیاید؟ چه زمانی یک learned rule وارد core می‌شود؟ چه زمانی رد می‌شود؟ چه زمانی فقط market-specific باقی می‌ماند؟ خیر. پاسخ متنی کافی است. `human_review_policy_v1.csv` `learned_rule_promotion_policy_v1.csv` `ai_recommendation_report_v1.csv` `branch_by_branch_validation_v1.csv`

## Concepts

[[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- AI-R03 — Human-in-the-Loop and Review Policy
  - Purpose
  - Required Clarifications
  - Image Requirement
  - Expected Derived Outputs

## Related Source Documents

- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[docs/experience_capture/questions/remaining_v2/by_code/AI-R03|AI-R03.md]] — score `10`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `10`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [[lab/03_experiments/EXP0000_sample/report|report.md]] — score `8`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|report.md]] — score `8`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
