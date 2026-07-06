---
title: "DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1600"
concepts:
  - "Convexity"
  - "Execution"
---


# DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy

**Source:** [[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa|docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1600` bytes

## خلاصه

چرا مهم است: چون در مدل تو سود فقط یک TP ثابت نیست؛ ممکن است چند مقصد، خروج پله‌ای، runner و tail داشته باشیم. این سیاست باید از سناریو و position جدا ولی متصل تعریف شود. برای پاسخ، حتماً این موارد را روشن کن: • TP اولیه کجا قرار می‌گیرد؟ • TP همیشه روی مقصد است یا کمی قبل/بعد از مقصد؟ • خروج پله‌ای چند مرحله‌ای چطور تصمیم‌گیری می‌شود؟ • چند درصد در مقصد اول، دوم، سوم بسته می‌شود؟ • خروج پله‌ای rule-based است یا trainable؟ • اگر مقصد اول نزدیک باشد ولی مقصد دوم خیلی باز باشد، چطور تصمیم می‌گیریم؟ • آیا می‌شود بخشی از معامله را برای tail / explosion باز گذاشت؟ • بعد از خروج اول، stop بقیه position چه می‌شود؟ • Break-even مجاز است یا با منطق convexity تضاد دارد؟ • خروج نهایی چه زمانی است؟ عکس

## Headings

- DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/RSK-R01/question_fa|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/RSK-R02/question_fa|RSK-R02 — Convexity Metrics and Cost-to-Potential Formula]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R03/question_fa|DST-R03 — Destination Repricing and Completion]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
