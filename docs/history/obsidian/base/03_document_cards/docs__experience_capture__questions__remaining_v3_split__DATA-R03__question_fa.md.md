---
title: "DATA-R03 — Training Granularity and Regime Weight Drift"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1305"
---


# DATA-R03 — Training Granularity and Regime Weight Drift

**Source:** [[docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_fa|docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1305` bytes

## خلاصه

چرا مهم است: چون گفتی شاید حتی در یک market/timeframe هم وزن‌ها ثابت نمانند. باید معلوم شود آموزش global، market-specific، timeframe-specific و dynamic weight regime چطور انجام می‌شود. برای پاسخ، حتماً این موارد را روشن کن: • Global training دقیقاً چه چیزهایی را یاد می‌گیرد؟ • Market-specific training چه زمانی لازم است؟ • Market-timeframe-specific training چه زمانی لازم است؟ • Dynamic weight regime یعنی چه؟ • Rolling windows چطور استفاده شوند؟ • Minimum sample برای اعتماد به وزن‌ها چقدر است؟ • Stability criteria چیست؟ • Drift detection چطور انجام شود؟ • Weight decay/boost چطور تعریف شود؟ • چه زمانی یک rule جهانی کنار گذاشته یا فقط local می‌شود؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد ا

## Headings

- DATA-R03 — Training Granularity and Regime Weight Drift

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R03/question_fa|AI-R03 — Human-in-the-Loop and Review Policy]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R03/question_fa|DST-R03 — Destination Repricing and Completion]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
