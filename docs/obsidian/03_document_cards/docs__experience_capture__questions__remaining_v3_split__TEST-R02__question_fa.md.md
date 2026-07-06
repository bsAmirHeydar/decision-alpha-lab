---
title: "TEST-R02 — Anti-Overfit, OOS, and Deployment Criteria"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1054"
concepts:
  - "Validation"
---


# TEST-R02 — Anti-Overfit, OOS, and Deployment Criteria

**Source:** [[docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_fa|docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1054` bytes

## خلاصه

چرا مهم است: چون اگر سیاست‌ها train می‌شوند، خطر overfit جدی است. باید معلوم شود چه زمانی یک rule یا policy واقعاً قابل اعتماد و deployable است. برای پاسخ، حتماً این موارد را روشن کن: • In-sample / out-of-sample split چطور باشد؟ • Walk-forward چطور طراحی شود؟ • Market split لازم است؟ • Timeframe split لازم است؟ • Regime split چطور تعریف شود؟ • Minimum sample size چقدر باشد؟ • Stability metrics چیست؟ • Failure cases چطور گزارش شوند؟ • Degradation tolerance چقدر است؟ • Deployment threshold چیست؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • anti_overfit_test_plan_v1.csv • oos_validation_policy_v1.csv • walk_forward_evaluation_v1.csv • deployment_criteria_v1.csv پاسخ شما:

## Headings

- TEST-R02 — Anti-Overfit, OOS, and Deployment Criteria

## Concepts

- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R03/question_fa|AI-R03 — Human-in-the-Loop and Review Policy]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_fa|EXE-R03 — Shadow, Paper, and Live Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_fa|DATA-R03 — Training Granularity and Regime Weight Drift]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
