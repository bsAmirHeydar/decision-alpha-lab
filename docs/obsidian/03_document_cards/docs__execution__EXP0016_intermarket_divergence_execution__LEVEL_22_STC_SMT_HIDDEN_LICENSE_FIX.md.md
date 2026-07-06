---
title: "Level 22 — STC SMT Hidden Offline License Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "3176"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Licensing"
  - "Validation"
---


# Level 22 — STC SMT Hidden Offline License Fix

**Source:** [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `3176` bytes

## خلاصه

این اصلاح برای پروژه‌ی STC / SMT Cycles است و عمداً inputهای لایسنس را مخفی/غیرمستقیم نگه می‌دارد. هیچ input واضحی با اسم license اضافه نمی‌شود. لایسنس همچنان از همین inputهای ظاهراً Cycle Model خوانده می‌شود: هیچ input واضحی با اسم مستقیم license اضافه نشده است. license engine حالا account-any را هم می‌فهمد. server-any از مقدار `ANY` پشتیبانی می‌کند. audit حالا دقیق‌تر می‌گوید mismatch از account است یا server یا signature یا gate. keygen خروجی recipient را فقط با inputهای مخفی `InpCycle...` چاپ می‌کند. bug تکرار دوباره‌ی نوشتن issuer audit در keygen حذف شد. برای لایسنسی که روی هر اکانت کار کند: خروجی recipient فقط این‌هاست: برای لایسنس محدود به اکانت خاص: برای bind به سرور خاص بروکر: اگر ل

## Headings

- Level 22 — STC SMT Hidden Offline License Fix
-   هدف
-   ورودی‌های مخفی لایسنس
-   چیزی که درست شد
-   account-any
-   account-bound
-   server-bound
-   نکته‌ی عیب‌یابی
-   مرزهای قفل‌شده

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|Level 02 — STC Time Engine and Cycle Classifier]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL 03 — STC SMT Check Candle Aggregator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|Level 04 — W Level Builder]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|Level 05 — STC SMT Reference Matrix and Raw Hunt Detector]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|Level 06 STC SMT Candidate Engine]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY|LEVEL 07 STC SMT Confirmation and Signal Registry]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|Level 08 STC SMT Risk Plan and Paper Entry]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL 09 — STC SMT Paper Outcome Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|Level 11 STC SMT Hard Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_12_STC_SMT_PERSISTENCE_RESTART_RECOVERY|Level 12 — STC SMT Persistence and Restart Recovery]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
