---
title: "ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "2427"
concepts:
  - "Convexity"
  - "Execution"
  - "Structural Nodes"
---


# ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

**Source:** [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `2427` bytes

## خلاصه

چرا مهم است: چون بعد از ساختن Limit Entry، هنوز معلوم نیست سفارش تا چه زمانی زنده است، چه زمانی باید کنسل شود، چه زمانی missed حساب شود، و چه زمانی با یک Entry-Level Extreme جدید جایگزین شود. این بخش جلوی اجرای کور و سفارش‌های مرده را می‌گیرد. برای پاسخ، حتماً این موارد را روشن کن: • وقتی parent zone سالم است ولی قیمت هنوز به limit نرسیده، سفارش تا چه زمانی زنده می‌ماند؟ • اگر سناریو، زون، یا محدودیت اصلی‌ای که سفارش را ساخته invalid شد، آیا pending limit فوراً cancel می‌شود؟ • اگر نود یا death boundary تایم ورود قبل از fill زده شد، سفارش چه وضعیتی می‌گیرد؟ • اگر قیمت بدون fill از زون برگشت و حرکت کرد، این missed است یا باید دنبال replace بگردیم؟ • Missed دقیقاً یعنی چه: حرکت به سمت مقصد بدو

## Headings

- ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/RSK-R01/question_fa|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/RSK-R02/question_fa|RSK-R02 — Convexity Metrics and Cost-to-Potential Formula]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
