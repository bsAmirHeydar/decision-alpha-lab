---
title: "AI-R03 — Human-in-the-Loop and Review Policy"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/AI-R03/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1217"
concepts:
  - "Validation"
---


# AI-R03 — Human-in-the-Loop and Review Policy

**Source:** [[docs/experience_capture/questions/remaining_v3_split/AI-R03/question_en|docs/experience_capture/questions/remaining_v3_split/AI-R03/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1217` bytes

## خلاصه

چون قبلاً گفتی اگر AI خلاف تجربه تو نتیجه بهتر گرفت، باید شرایط قبولش مشخص باشد. باید فرق recommendation، auto-apply، branch test و core promotion روشن شود. وقتی AI خلاف تجربه تو نتیجه بهتر گرفت، کجا قابل قبول است؟ چه سطح شواهدی لازم است؟ کدام تغییرات فقط recommendation هستند؟ کدام تغییرات می‌توانند auto-apply شوند؟ Branch-by-branch test لازم است؟ آیا چند الگوریتم باید یک نتیجه را تأیید کنند؟ چه چیزهایی باید در گزارش انسانی بیاید؟ چه زمانی یک learned rule وارد core می‌شود؟ چه زمانی رد می‌شود؟ چه زمانی فقط market-specific باقی می‌ماند؟ خیر. پاسخ متنی کافی است. `human_review_policy_v1.csv` `learned_rule_promotion_policy_v1.csv` `ai_recommendation_report_v1.csv` `branch_by_branch_validation_v1.

## Headings

- AI-R03 — Human-in-the-Loop and Review Policy
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
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_en|EXE-R03 — Shadow, Paper, and Live Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
