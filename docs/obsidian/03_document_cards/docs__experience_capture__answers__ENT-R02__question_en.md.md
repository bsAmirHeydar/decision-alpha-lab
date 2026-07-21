---
title: "ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/ENT-R02/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1171"
concepts:
  - "Convexity"
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy

**Source:** [[docs/experience_capture/answers/ENT-R02/question_en|docs/experience_capture/answers/ENT-R02/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1171` bytes

## خلاصه

When a valid Entry-Level Extreme / Extreme Near Death exists inside a zone, how should limit entry, stop geometry, spread adjustment, buffer, fill policy, and order splitting be defined? ENT-R01 defined the entry-level Extreme as Extreme Near Death: an entry-scale CycleHook excessively close to death, used to reduce stop size and improve convexity. ENT-R02 defines the practical limit-order geometry and execution-intent rules around that concept. Please clarify: Where is the limit entry placed? Where is the stop placed? Is there a buffer behind the stop? Is the buffer fixed or trainable? How should spread be handled for buy limit and sell limit? Should broker constraints be part of NDS or exe

## Headings

- ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy
-   Question
-   Why This Question Remains
-   Answer Requirements
-   Expected Output

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/question_en|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R03/question_en|SCN-R03 — Scenario Ranking and Multi-Zone Selection]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R04/question_en|SCN-R04 — Scenario Update, Death, and Repricing]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_en|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
