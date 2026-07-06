---
title: "EXE-R02 — Broker Validator and Send Gate"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1320"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Validation"
---


# EXE-R02 — Broker Validator and Send Gate

**Source:** [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa|docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1320` bytes

## خلاصه

چرا مهم است: چون حتی اگر NDS یک intent عالی بسازد، broker ممکن است به خاطر min stop، tick، margin، freeze level یا max lot اجازه اجرا ندهد. این لایه باید جلوی اجرای خراب را بگیرد. برای پاسخ، حتماً این موارد را روشن کن: • کدام broker constraints باید حتماً چک شوند؟ • Min stop distance چطور با structural stop مقایسه می‌شود؟ • Tick size و digits چطور normalize می‌شوند؟ • Lot step، min lot و max lot چطور اعمال می‌شوند؟ • Margin کافی نبود، intent veto می‌شود یا حجم adjust می‌شود؟ • Spread چه زمانی باعث veto می‌شود؟ • Freeze level و trade mode چطور لحاظ می‌شوند؟ • Market open/session مهم است؟ • Order rejection handling چطور باشد؟ • چه زمانی adjust مجاز است و چه زمانی veto؟ عکس لازم: خیر. پاسخ متنی

## Headings

- EXE-R02 — Broker Validator and Send Gate

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_fa|EXE-R03 — Shadow, Paper, and Live Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_fa|SYS-R01 — Final NDS Architecture and Build Order]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
