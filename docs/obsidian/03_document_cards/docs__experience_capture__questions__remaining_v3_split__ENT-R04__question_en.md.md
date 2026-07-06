---
title: "ENT-R04 — After Fill: Scenario-to-Position Transition"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1970"
concepts:
  - "Execution"
  - "Structural Nodes"
  - "Validation"
---


# ENT-R04 — After Fill: Scenario-to-Position Transition

**Source:** [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en|docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1970` bytes

## خلاصه

چون وقتی limit پر شد، سیستم از تحلیل و intent وارد position واقعی می‌شود. باید معلوم باشد بعد از fill، سناریو هنوز زنده است، تبدیل به position thread می‌شود، یا وارد مدیریت مستقل معامله می‌شود. بعد از fill، ScenarioThread همچنان زنده می‌ماند یا به PositionThread تبدیل می‌شود؟ اگر parent scenario بعد از ورود ضعیف شد، position چه واکنشی دارد؟ اگر سناریوی مخالف بعد از ورود قوی‌تر شد، position کاهش پیدا می‌کند، hedge می‌شود، یا فقط با stop/TP مدیریت می‌شود؟ استاپ بعد از fill ثابت می‌ماند یا با ساختار جدید می‌تواند جابه‌جا شود؟ اگر مقصد اول خورده شد، position partially completed می‌شود یا سناریو همچنان زنده است؟ خروج پله‌ای جزو scenario است یا position management؟ اگر چند entry داخل یک zone داریم

## Headings

- ENT-R04 — After Fill: Scenario-to-Position Transition
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
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`
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
