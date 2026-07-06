---
title: "DATA-R03 — Training Granularity and Regime Weight Drift"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1191"
---


# DATA-R03 — Training Granularity and Regime Weight Drift

**Source:** [[docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_en|docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1191` bytes

## خلاصه

چون گفتی شاید حتی در یک market/timeframe هم وزن‌ها ثابت نمانند. باید معلوم شود آموزش global، market-specific، timeframe-specific و dynamic weight regime چطور انجام می‌شود. Global training دقیقاً چه چیزهایی را یاد می‌گیرد؟ Market-specific training چه زمانی لازم است؟ Market-timeframe-specific training چه زمانی لازم است؟ Dynamic weight regime یعنی چه؟ Rolling windows چطور استفاده شوند؟ Minimum sample برای اعتماد به وزن‌ها چقدر است؟ Stability criteria چیست؟ Drift detection چطور انجام شود؟ Weight decay/boost چطور تعریف شود؟ چه زمانی یک rule جهانی کنار گذاشته یا فقط local می‌شود؟ خیر. پاسخ متنی کافی است. `training_granularity_model_v1.csv` `market_timeframe_policy_v1.csv` `dynamic_weight_regime_mo

## Headings

- DATA-R03 — Training Granularity and Regime Weight Drift
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Related documents

- [[docs/experience_capture/answers/BASE-02/question_en|BASE-02 — What Exactly Is a Scenario?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/question_en|BASE-03 — What Counts as a Valid Reason, and What Is Only Noise?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/question_en|BASE-04 — Which Concepts Must Never Enter the System?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/question_en|BASE-05 — How Far Is Uncertainty Allowed?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/question_en|BASE-06 — What Should Be a Hard Rule, and What Should Remain Learnable?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R02/question_en|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/question_en|DST-R03 — Destination Repricing and Completion]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
