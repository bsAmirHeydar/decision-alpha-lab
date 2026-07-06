---
title: "TEST-R02 — Anti-Overfit, OOS, and Deployment Criteria"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "940"
concepts:
  - "Validation"
---


# TEST-R02 — Anti-Overfit, OOS, and Deployment Criteria

**Source:** [[docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_en|docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `940` bytes

## خلاصه

چون اگر سیاست‌ها train می‌شوند، خطر overfit جدی است. باید معلوم شود چه زمانی یک rule یا policy واقعاً قابل اعتماد و deployable است. In-sample / out-of-sample split چطور باشد؟ Walk-forward چطور طراحی شود؟ Market split لازم است؟ Timeframe split لازم است؟ Regime split چطور تعریف شود؟ Minimum sample size چقدر باشد؟ Stability metrics چیست؟ Failure cases چطور گزارش شوند؟ Degradation tolerance چقدر است؟ Deployment threshold چیست؟ خیر. پاسخ متنی کافی است. `anti_overfit_test_plan_v1.csv` `oos_validation_policy_v1.csv` `walk_forward_evaluation_v1.csv` `deployment_criteria_v1.csv`

## Headings

- TEST-R02 — Anti-Overfit, OOS, and Deployment Criteria
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/DST-R03/question_en|DST-R03 — Destination Repricing and Completion]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-06/question_en|EXT-06 — If Price Slightly Penetrates the Node and Quickly Returns, Is the Extreme Invalid?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_en|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R03/question_en|AI-R03 — Human-in-the-Loop and Review Policy]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_en|EXE-R03 — Shadow, Paper, and Live Transition]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
