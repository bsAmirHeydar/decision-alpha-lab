---
title: "ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "2313"
concepts:
  - "Convexity"
  - "Execution"
  - "Structural Nodes"
---


# ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

**Source:** [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_en|docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `2313` bytes

## خلاصه

چون بعد از ساختن Limit Entry، هنوز معلوم نیست سفارش تا چه زمانی زنده است، چه زمانی باید کنسل شود، چه زمانی missed حساب شود، و چه زمانی با یک Entry-Level Extreme جدید جایگزین شود. این بخش جلوی اجرای کور و سفارش‌های مرده را می‌گیرد. وقتی parent zone سالم است ولی قیمت هنوز به limit نرسیده، سفارش تا چه زمانی زنده می‌ماند؟ اگر سناریو، زون، یا محدودیت اصلی‌ای که سفارش را ساخته invalid شد، آیا pending limit فوراً cancel می‌شود؟ اگر نود یا death boundary تایم ورود قبل از fill زده شد، سفارش چه وضعیتی می‌گیرد؟ اگر قیمت بدون fill از زون برگشت و حرکت کرد، این missed است یا باید دنبال replace بگردیم؟ Missed دقیقاً یعنی چه: حرکت به سمت مقصد بدون fill، خروج از زون، یا بسته‌شدن entry window؟ Replace دقیقاً

## Headings

- ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/question_en|RSK-R02 — Convexity Metrics and Cost-to-Potential Formula]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/question_en|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R03/question_en|SCN-R03 — Scenario Ranking and Multi-Zone Selection]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R04/question_en|SCN-R04 — Scenario Update, Death, and Repricing]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_en|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_en|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
