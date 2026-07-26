# AI-R03 — Human-in-the-Loop and Review Policy

## Purpose
چون قبلاً گفتی اگر AI خلاف تجربه تو نتیجه بهتر گرفت، باید شرایط قبولش مشخص باشد. باید فرق recommendation، auto-apply، branch test و core promotion روشن شود.

## Required Clarifications
- وقتی AI خلاف تجربه تو نتیجه بهتر گرفت، کجا قابل قبول است؟
- چه سطح شواهدی لازم است؟
- کدام تغییرات فقط recommendation هستند؟
- کدام تغییرات می‌توانند auto-apply شوند؟
- Branch-by-branch test لازم است؟
- آیا چند الگوریتم باید یک نتیجه را تأیید کنند؟
- چه چیزهایی باید در گزارش انسانی بیاید؟
- چه زمانی یک learned rule وارد core می‌شود؟
- چه زمانی رد می‌شود؟
- چه زمانی فقط market-specific باقی می‌ماند؟

## Image Requirement
خیر. پاسخ متنی کافی است.

## Expected Derived Outputs
- `human_review_policy_v1.csv`
- `learned_rule_promotion_policy_v1.csv`
- `ai_recommendation_report_v1.csv`
- `branch_by_branch_validation_v1.csv`
