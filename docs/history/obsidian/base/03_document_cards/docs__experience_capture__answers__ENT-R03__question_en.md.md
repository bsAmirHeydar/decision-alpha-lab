---
title: "ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/ENT-R03/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1637"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

**Source:** [[docs/experience_capture/answers/ENT-R03/question_en|docs/experience_capture/answers/ENT-R03/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1637` bytes

## خلاصه

After a Limit Entry is created from a valid Entry-Level Extreme, how long should the pending limit remain alive, when should it be canceled or deleted, and how should missed or replacement behavior be defined? ENT-R01 defined the Entry-Level Extreme as Extreme Near Death. ENT-R02 defined the practical entry geometry: limit entry, stop behind node, trainable buffer, spread adjustment, and max-lot splitting. ENT-R03 defines the lifecycle of the pending limit before fill. Please clarify: While the parent zone is alive but price has not reached the limit, how long does the pending order remain alive? If the scenario, zone, or original reason that created the order becomes invalid, should the pen

## Headings

- ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace
-   Question
-   Why This Question Remains
-   Answer Requirements
-   Expected Output

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
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
