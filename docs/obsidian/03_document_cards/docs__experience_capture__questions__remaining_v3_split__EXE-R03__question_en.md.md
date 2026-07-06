---
title: "EXE-R03 — Shadow, Paper, and Live Transition"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1165"
concepts:
  - "Execution"
  - "Validation"
---


# EXE-R03 — Shadow, Paper, and Live Transition

**Source:** [[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_en|docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1165` bytes

## خلاصه

چون سیستم باید مرحله‌ای جلو برود؛ اول shadow، بعد paper، بعد live. هر مرحله باید معیار عبور، safety gate و kill switch داشته باشد. Shadow mode دقیقاً چه چیزهایی را log می‌کند؟ Paper mode چه تفاوتی با shadow دارد؟ Live mode چه safety gateهایی می‌خواهد؟ AI در live فقط rank/veto می‌کند یا نقش دیگری هم دارد؟ چه metricهایی برای رفتن از shadow به paper لازم است؟ چه metricهایی برای رفتن از paper به live لازم است؟ چه kill switchهایی لازم است؟ اگر مدل drift کرد، به کدام mode برمی‌گردد؟ هر market/timeframe جدا approval می‌خواهد؟ Audit برای هر intent و order چگونه است؟ خیر. پاسخ متنی کافی است. `shadow_mode_policy_v1.csv` `paper_mode_policy_v1.csv` `live_gate_policy_v1.csv` `kill_switch_policy_v1.csv`

## Headings

- EXE-R03 — Shadow, Paper, and Live Transition
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-06/question_en|EXT-06 — If Price Slightly Penetrates the Node and Quickly Returns, Is the Extreme Invalid?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_en|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_en|EXE-R02 — Broker Validator and Send Gate]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/question_en|BASE-02 — What Exactly Is a Scenario?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/question_en|BASE-03 — What Counts as a Valid Reason, and What Is Only Noise?]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
