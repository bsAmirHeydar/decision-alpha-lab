---
title: "EXE-R04 — Execution Audit and Reconciliation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1261"
concepts:
  - "Execution"
  - "Structural Nodes"
  - "Validation"
---


# EXE-R04 — Execution Audit and Reconciliation

**Source:** [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa|docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1261` bytes

## خلاصه

چرا مهم است: چون باید بفهمیم سیستم چه قصدی داشته، چه چیزی به broker فرستاده شده، چه چیزی fill شده و اختلاف‌ها از کجا آمده‌اند. بدون reconciliation، backtest/paper/live قابل اعتماد نیست. برای پاسخ، حتماً این موارد را روشن کن: • Intent price و submitted price چطور مقایسه می‌شوند؟ • Submitted price و filled price چطور مقایسه می‌شوند؟ • Structural SL/TP و adjusted SL/TP جدا ذخیره شوند؟ • Slippage چطور ثبت شود؟ • Partial fills چطور ثبت شوند؟ • Rejected orders چطور ثبت شوند؟ • Canceled orders چطور ثبت شوند؟ • Split order aggregation چطور باشد؟ • Broker-side modification چطور audit شود؟ • Reconciliation با scenario/zone/entry ID چطور انجام شود؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار ب

## Headings

- EXE-R04 — Execution Audit and Reconciliation

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_fa|EXE-R03 — Shadow, Paper, and Live Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_fa|SYS-R01 — Final NDS Architecture and Build Order]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa|TEST-R01 — Baseline, Ablation, and Family Testing]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
