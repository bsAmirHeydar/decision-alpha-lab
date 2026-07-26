---
title: "TEST-R01 — Baseline, Ablation, and Family Testing"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1128"
concepts:
  - "Execution"
  - "Hook"
  - "Rally"
  - "Structural Nodes"
---


# TEST-R01 — Baseline, Ablation, and Family Testing

**Source:** [[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa|docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1128` bytes

## خلاصه

چرا مهم است: چون برای فهمیدن ارزش واقعی هر قید باید آن را جدا، ترکیبی، با و بدون بقیه تست کنیم. بدون ablation معلوم نمی‌شود کدام رشته واقعاً edge می‌دهد. برای پاسخ، حتماً این موارد را روشن کن: • Baseline pure Hook چطور باشد؟ • Baseline pure Rally/F چطور باشد؟ • X-only چطور تست شود؟ • Y-only چطور تست شود؟ • XY چطور تست شود؟ • Symmetry-only یا symmetry-added چطور تست شود؟ • Zone with/without destination چطور مقایسه شود؟ • Entry with/without near-death چطور مقایسه شود؟ • Buffer variants چطور تست شوند؟ • Global vs market-specific results چطور مقایسه شوند؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • baseline_experiment_plan_v1.csv • ablation_matrix_v1.csv • family_comparis

## Headings

- TEST-R01 — Baseline, Ablation, and Family Testing

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_fa|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_fa|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_fa|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|AI-R01 — AI Boundary and Allowed Decisions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R02/question_fa|AI-R02 — Training Targets and Model Families]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R04/question_fa|DATA-R04 — Evaluation Metrics: Before and After Convexity]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R03/question_fa|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_fa|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_fa|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa|EXE-R04 — Execution Audit and Reconciliation]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_fa|SYS-R01 — Final NDS Architecture and Build Order]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R02/question_fa|DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
