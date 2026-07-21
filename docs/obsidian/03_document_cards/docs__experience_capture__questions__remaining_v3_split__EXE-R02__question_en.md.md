---
title: "EXE-R02 — Broker Validator and Send Gate"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1206"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Validation"
---


# EXE-R02 — Broker Validator and Send Gate

**Source:** [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_en|docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1206` bytes

## خلاصه

چون حتی اگر NDS یک intent عالی بسازد، broker ممکن است به خاطر min stop، tick، margin، freeze level یا max lot اجازه اجرا ندهد. این لایه باید جلوی اجرای خراب را بگیرد. کدام broker constraints باید حتماً چک شوند؟ Min stop distance چطور با structural stop مقایسه می‌شود؟ Tick size و digits چطور normalize می‌شوند؟ Lot step، min lot و max lot چطور اعمال می‌شوند؟ Margin کافی نبود، intent veto می‌شود یا حجم adjust می‌شود؟ Spread چه زمانی باعث veto می‌شود؟ Freeze level و trade mode چطور لحاظ می‌شوند؟ Market open/session مهم است؟ Order rejection handling چطور باشد؟ چه زمانی adjust مجاز است و چه زمانی veto؟ خیر. پاسخ متنی کافی است. `broker_validation_model_v1.csv` `send_gate_policy_v1.csv` `execution_v

## Headings

- EXE-R02 — Broker Validator and Send Gate
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-06/question_en|EXT-06 — If Price Slightly Penetrates the Node and Quickly Returns, Is the Extreme Invalid?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R02/question_en|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/question_en|EXT-01 — How Exactly Is Extreme Defined Relative to an Untouched Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-02/question_en|EXT-02 — Which Project Logic Produces the Anchor Node for Extreme?]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
