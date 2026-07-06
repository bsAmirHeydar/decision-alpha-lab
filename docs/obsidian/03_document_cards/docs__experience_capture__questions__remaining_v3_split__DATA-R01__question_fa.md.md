---
title: "DATA-R01 — Canonical State Packet v1"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1222"
concepts:
  - "Convexity"
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# DATA-R01 — Canonical State Packet v1

**Source:** [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1222` bytes

## خلاصه

چرا مهم است: چون rule engine، AI، backtest، shadow، paper و execution باید همه از یک زبان مشترک استفاده کنند. این زبان همان state packet استاندارد NDS است. برای پاسخ، حتماً این موارد را روشن کن: • در هر لحظه، Node state باید چه فیلدهایی داشته باشد؟ • CycleHook state شامل چه چیزهایی باشد؟ • Sequence state، X/Y closure و Hook type چطور ذخیره شوند؟ • Context/position چطور وارد packet شود؟ • Zone candidates چطور ثبت شوند؟ • Scenario threads چطور ثبت شوند؟ • Entry extremes و ExecutionIntentها چطور وصل شوند؟ • Destinations و optionality چطور ذخیره شوند؟ • Risk state و pending orders چطور وارد packet شوند؟ • Parent-child fractal relations چطور استاندارد شوند؟ عکس لازم: خیر. پاسخ متنی کافی است. خروج

## Headings

- DATA-R01 — Canonical State Packet v1

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_fa|SYS-R01 — Final NDS Architecture and Build Order]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa|TEST-R01 — Baseline, Ablation, and Family Testing]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/RSK-R01/question_fa|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/RSK-R02/question_fa|RSK-R02 — Convexity Metrics and Cost-to-Potential Formula]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
