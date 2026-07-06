---
title: "EXE-R04 — Execution Audit and Reconciliation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1147"
concepts:
  - "Execution"
  - "Structural Nodes"
  - "Validation"
---


# EXE-R04 — Execution Audit and Reconciliation

**Source:** [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en|docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1147` bytes

## خلاصه

چون باید بفهمیم سیستم چه قصدی داشته، چه چیزی به broker فرستاده شده، چه چیزی fill شده و اختلاف‌ها از کجا آمده‌اند. بدون reconciliation، backtest/paper/live قابل اعتماد نیست. Intent price و submitted price چطور مقایسه می‌شوند؟ Submitted price و filled price چطور مقایسه می‌شوند؟ Structural SL/TP و adjusted SL/TP جدا ذخیره شوند؟ Slippage چطور ثبت شود؟ Partial fills چطور ثبت شوند؟ Rejected orders چطور ثبت شوند؟ Canceled orders چطور ثبت شوند؟ Split order aggregation چطور باشد؟ Broker-side modification چطور audit شود؟ Reconciliation با scenario/zone/entry ID چطور انجام شود؟ خیر. پاسخ متنی کافی است. `execution_audit_ledger_v1.csv` `intent_to_order_reconciliation_v1.csv` `fill_quality_model_v1.csv` `

## Headings

- EXE-R04 — Execution Audit and Reconciliation
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_en|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R04/question_en|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/question_en|EXT-01 — How Exactly Is Extreme Defined Relative to an Untouched Node?]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
