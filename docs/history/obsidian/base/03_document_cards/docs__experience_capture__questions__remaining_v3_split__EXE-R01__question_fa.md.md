---
title: "EXE-R01 — ExecutionIntent Contract Finalization"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1336"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# EXE-R01 — ExecutionIntent Contract Finalization

**Source:** [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1336` bytes

## خلاصه

چرا مهم است: چون سیستم نباید مستقیم order بفرستد. NDS باید فقط ExecutionIntent بسازد و validator تصمیم بگیرد که قابل ارسال هست یا نه. پس قرارداد intent باید دقیق باشد. برای پاسخ، حتماً این موارد را روشن کن: • حداقل فیلدهای اجباری ExecutionIntent چیست؟ • scenario_id، zone_id، entry_extreme_id، node_id و destination_id چطور به هم وصل می‌شوند؟ • Structural price و adjusted price جدا ذخیره شوند؟ • Spread adjustment کجا ثبت شود؟ • Stop buffer و دلیلش کجا ثبت شود؟ • Risk budget و volume چطور ثبت شود؟ • Split orders داخل همان intent باشند یا child intents؟ • Cancel/replace/missed conditions داخل intent باشند؟ • Intent بدون broker validation قابل اجرا نیست؟ • چه چیزی intent را unsafe می‌کند؟ عکس لاز

## Headings

- EXE-R01 — ExecutionIntent Contract Finalization

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_fa|SYS-R01 — Final NDS Architecture and Build Order]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_fa|EXE-R03 — Shadow, Paper, and Live Transition]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
