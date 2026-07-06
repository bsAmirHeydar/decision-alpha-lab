---
title: "SYS-R01 — Final NDS Architecture and Build Order"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1254"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# SYS-R01 — Final NDS Architecture and Build Order

**Source:** [[docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_fa|docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1254` bytes

## خلاصه

چرا مهم است: چون بعد از ثبت ontology، سناریو، زون، ورود، ریسک، execution، data و AI باید ترتیب ساخت مشخص شود. بدون build order، پروژه سنگین و پراکنده می‌شود. برای پاسخ، حتماً این موارد را روشن کن: • اول object builderها ساخته شوند یا execution layer؟ • Canonical State Packet قبل از AI لازم است؟ • Event ledger قبل از training لازم است؟ • Scenario/Zone/Entry layer قبل از backtest چطور ساخته شود؟ • UI لازم است یا بعداً؟ • Shadow/Paper/Live gate در چه مرحله‌ای می‌آید؟ • کدام بخش‌ها hard rule هستند؟ • کدام بخش‌ها trainable هستند؟ • کدام بخش‌ها فعلاً فقط مستندسازی شوند؟ • Roadmap نهایی ساخت سیستم چیست؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • nds_build_order_v1.csv • sys

## Headings

- SYS-R01 — Final NDS Architecture and Build Order

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa|TEST-R01 — Baseline, Ablation, and Family Testing]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
