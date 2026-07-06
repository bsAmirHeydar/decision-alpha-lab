---
title: "DATA-R04 — Evaluation Metrics: Before and After Convexity"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1172"
concepts:
  - "Convexity"
  - "Execution"
  - "Structural Nodes"
---


# DATA-R04 — Evaluation Metrics: Before and After Convexity

**Source:** [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_en|docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1172` bytes

## خلاصه

چون اگر win rate قبل از convexity اولویت ندارد، گزارش‌گیری و ارزیابی هم باید convexity-first باشد. باید pre-convexity و post-convexity metrics جدا شوند. Pre-convexity filters چه چیزهایی هستند؟ Post-convexity win rate دقیقاً روی کدام subset محاسبه می‌شود؟ R distribution چطور ثبت شود؟ Tail contribution چطور سنجیده شود؟ Missed opportunity چطور حساب شود؟ Fill probability چقدر مهم است؟ Stop buffer performance چطور سنجیده شود؟ Zone family performance چطور گزارش شود؟ Scenario family performance چطور گزارش شود؟ Market/timeframe breakdown چطور باشد؟ خیر. اگر گزارش یا equity/R distribution داری، اختیاری مفید است. `convexity_first_evaluation_v1.csv` `post_convexity_win_rate_model_v1.csv` `tail_contribu

## Headings

- DATA-R04 — Evaluation Metrics: Before and After Convexity
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/question_en|RSK-R02 — Convexity Metrics and Cost-to-Potential Formula]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/question_en|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R03/question_en|SCN-R03 — Scenario Ranking and Multi-Zone Selection]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R04/question_en|SCN-R04 — Scenario Update, Death, and Repricing]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_en|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
