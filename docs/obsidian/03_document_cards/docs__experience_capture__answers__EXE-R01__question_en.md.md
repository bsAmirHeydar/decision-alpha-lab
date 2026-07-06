---
title: "EXE-R01 — ExecutionIntent Contract Finalization"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/EXE-R01/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1278"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# EXE-R01 — ExecutionIntent Contract Finalization

**Source:** [[docs/experience_capture/answers/EXE-R01/question_en|docs/experience_capture/answers/EXE-R01/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1278` bytes

## خلاصه

What should the ExecutionIntent contract contain, and how should NDS convert structural analysis into a safe executable intent without sending broker orders directly? Previous records established that NDS should not directly send orders. It should produce a structured ExecutionIntent that is later validated by broker and safety layers. However, the exact field-level contract is not fully known yet. This question captures the current known boundary: the intent must be derived from the fractal four-state view through context, zone, and entry quality. Please clarify: What is known about the structure behind ExecutionIntent? Should the four-state view be read fractally? How does the four-state v

## Headings

- EXE-R01 — ExecutionIntent Contract Finalization
-   Question
-   Why This Question Remains
-   Answer Requirements
-   Expected Output

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/question_en|EXT-01 — How Exactly Is Extreme Defined Relative to an Untouched Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-09/question_en|EXT-09 — How Do You Understand the Quality of the Anchor Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/question_en|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R03/question_en|SCN-R03 — Scenario Ranking and Multi-Zone Selection]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R04/question_en|SCN-R04 — Scenario Update, Death, and Repricing]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
