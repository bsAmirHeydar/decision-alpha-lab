---
title: "DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/DST-R02/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1486"
concepts:
  - "Convexity"
  - "Execution"
---


# DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy

**Source:** [[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_en|docs/experience_capture/questions/remaining_v3_split/DST-R02/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1486` bytes

## خلاصه

چون در مدل تو سود فقط یک TP ثابت نیست؛ ممکن است چند مقصد، خروج پله‌ای، runner و tail داشته باشیم. این سیاست باید از سناریو و position جدا ولی متصل تعریف شود. TP اولیه کجا قرار می‌گیرد؟ TP همیشه روی مقصد است یا کمی قبل/بعد از مقصد؟ خروج پله‌ای چند مرحله‌ای چطور تصمیم‌گیری می‌شود؟ چند درصد در مقصد اول، دوم، سوم بسته می‌شود؟ خروج پله‌ای rule-based است یا trainable؟ اگر مقصد اول نزدیک باشد ولی مقصد دوم خیلی باز باشد، چطور تصمیم می‌گیریم؟ آیا می‌شود بخشی از معامله را برای tail / explosion باز گذاشت؟ بعد از خروج اول، stop بقیه position چه می‌شود؟ Break-even مجاز است یا با منطق convexity تضاد دارد؟ خروج نهایی چه زمانی است؟ اختیاری. اگر نمونه چند مقصد و خروج پله‌ای داری، عکس کمک می‌کند. `take_profit

## Headings

- DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]

## Related documents

- [[docs/experience_capture/answers/BASE-02/question_en|BASE-02 — What Exactly Is a Scenario?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/question_en|BASE-03 — What Counts as a Valid Reason, and What Is Only Noise?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/question_en|BASE-05 — How Far Is Uncertainty Allowed?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R02/question_en|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-11/question_en|EXT-11 — Does Extreme Only Make Sense When Entering Against the Current Move?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/question_en|RSK-R02 — Convexity Metrics and Cost-to-Potential Formula]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/question_en|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
