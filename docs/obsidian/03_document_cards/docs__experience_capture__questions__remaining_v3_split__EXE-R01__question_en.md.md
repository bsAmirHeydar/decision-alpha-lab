---
title: "EXE-R01 — ExecutionIntent Contract Finalization"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1222"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# EXE-R01 — ExecutionIntent Contract Finalization

**Source:** [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1222` bytes

## خلاصه

چون سیستم نباید مستقیم order بفرستد. NDS باید فقط ExecutionIntent بسازد و validator تصمیم بگیرد که قابل ارسال هست یا نه. پس قرارداد intent باید دقیق باشد. حداقل فیلدهای اجباری ExecutionIntent چیست؟ scenario_id، zone_id، entry_extreme_id، node_id و destination_id چطور به هم وصل می‌شوند؟ Structural price و adjusted price جدا ذخیره شوند؟ Spread adjustment کجا ثبت شود؟ Stop buffer و دلیلش کجا ثبت شود؟ Risk budget و volume چطور ثبت شود؟ Split orders داخل همان intent باشند یا child intents؟ Cancel/replace/missed conditions داخل intent باشند؟ Intent بدون broker validation قابل اجرا نیست؟ چه چیزی intent را unsafe می‌کند؟ خیر. پاسخ متنی کافی است. `execution_intent_contract_v1.csv` `execution_intent_l

## Headings

- EXE-R01 — ExecutionIntent Contract Finalization
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/question_en|EXT-01 — How Exactly Is Extreme Defined Relative to an Untouched Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-06/question_en|EXT-06 — If Price Slightly Penetrates the Node and Quickly Returns, Is the Extreme Invalid?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-09/question_en|EXT-09 — How Do You Understand the Quality of the Anchor Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
