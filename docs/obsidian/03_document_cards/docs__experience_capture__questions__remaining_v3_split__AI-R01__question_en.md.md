---
title: "AI-R01 — AI Boundary and Allowed Decisions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/AI-R01/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1162"
concepts:
  - "Execution"
  - "Structural Nodes"
  - "Validation"
---


# AI-R01 — AI Boundary and Allowed Decisions

**Source:** [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_en|docs/experience_capture/questions/remaining_v3_split/AI-R01/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1162` bytes

## خلاصه

چون AI نباید ontology را خراب کند یا نقش decision god بگیرد. باید دقیق مشخص شود AI چه کارهایی مجاز است انجام دهد و چه چیزهایی hard rule باقی می‌ماند. AI مجاز است ontology را تغییر دهد یا فقط پیشنهاد بدهد؟ AI فقط rank/veto/select/score می‌کند؟ AI می‌تواند zone family جدید پیشنهاد دهد؟ AI می‌تواند entry را replace کند؟ AI می‌تواند risk budget پیشنهاد دهد؟ AI می‌تواند order send کند؟ طبق معماری فعلی جواب پیش‌فرض: نه. چه چیزهایی hard rule هستند؟ چه چیزهایی learnable policy هستند؟ AI output باید explainable باشد؟ هر تصمیم AI چطور audit می‌شود؟ خیر. پاسخ متنی کافی است. `ai_boundary_model_v1.csv` `ai_allowed_actions_v1.csv` `ai_veto_rank_select_policy_v1.csv` `ai_audit_contract_v1.csv`

## Headings

- AI-R01 — AI Boundary and Allowed Decisions
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
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
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
