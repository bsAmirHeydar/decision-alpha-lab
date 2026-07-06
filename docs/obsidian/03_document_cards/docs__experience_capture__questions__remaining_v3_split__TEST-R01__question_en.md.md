---
title: "TEST-R01 — Baseline, Ablation, and Family Testing"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1014"
concepts:
  - "Execution"
  - "Hook"
  - "Rally"
  - "Structural Nodes"
---


# TEST-R01 — Baseline, Ablation, and Family Testing

**Source:** [[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_en|docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1014` bytes

## خلاصه

چون برای فهمیدن ارزش واقعی هر قید باید آن را جدا، ترکیبی، با و بدون بقیه تست کنیم. بدون ablation معلوم نمی‌شود کدام رشته واقعاً edge می‌دهد. Baseline pure Hook چطور باشد؟ Baseline pure Rally/F چطور باشد؟ X-only چطور تست شود؟ Y-only چطور تست شود؟ XY چطور تست شود؟ Symmetry-only یا symmetry-added چطور تست شود؟ Zone with/without destination چطور مقایسه شود؟ Entry with/without near-death چطور مقایسه شود؟ Buffer variants چطور تست شوند؟ Global vs market-specific results چطور مقایسه شوند؟ خیر. پاسخ متنی کافی است. `baseline_experiment_plan_v1.csv` `ablation_matrix_v1.csv` `family_comparison_report_v1.csv`

## Headings

- TEST-R01 — Baseline, Ablation, and Family Testing
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-02/question_en|EXT-02 — Which Project Logic Produces the Anchor Node for Extreme?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_en|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R04/question_en|ENT-R04 — After Fill: Scenario-to-Position Transition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
