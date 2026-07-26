
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX.md"
source_ext: ".md"
source_size: 3176
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Licensing", "Python Brain", "Validation / Audit"]
entities: []
---

# Source Card — LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX.md]]

## Summary

این اصلاح برای پروژه‌ی STC / SMT Cycles است و عمداً inputهای لایسنس را مخفی/غیرمستقیم نگه می‌دارد. هیچ input واضحی با اسم license اضافه نمی‌شود. لایسنس همچنان از همین inputهای ظاهراً Cycle Model خوانده می‌شود: هیچ input واضحی با اسم مستقیم license اضافه نشده است. license engine حالا account-any را هم می‌فهمد. server-any از مقدار `ANY` پشتیبانی می‌کند. audit حالا دقیق‌تر می‌گوید mismatch از account است یا server یا signature یا gate. keygen خروجی recipient را فقط با inputهای مخفی `InpCycle...` چاپ می‌کند. bug تکرار دوباره‌ی نوشتن issuer audit در keygen حذف شد. برای لایسنسی که روی هر اکانت کار کند: خروجی recipient فقط این‌هاست: برای لایسنس محدود به اکانت خاص: برای bind به سرور خاص بروکر: اگر لایسنس بالا نیاید، داخل Experts log خط `STC_LICENSE` را ببین. reasonهای مهم: این خروجی‌ها نشان می‌دهند دقیقاً کدام input اشتباه وارد شده یا bind درست نیست. این اصلاح هیچ‌کدام از این منطق‌ها را تغییر نم

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 22 — STC SMT Hidden Offline License Fix
  - هدف
  - ورودی‌های مخفی لایسنس
  - چیزی که درست شد
  - account-any
  - account-bound
  - server-bound
  - نکته‌ی عیب‌یابی
  - مرزهای قفل‌شده

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20_PAPER_PORTFOLIO_AGGREGATE_METRICS|FLAG_COUNTING_LEVEL_19_PHASE20_PAPER_PORTFOLIO_AGGREGATE_METRICS.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `10`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `10`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `9`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]] — score `9`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|LEVEL_04_STC_SMT_W_LEVEL_BUILDER.md]] — score `9`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] — score `9`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
