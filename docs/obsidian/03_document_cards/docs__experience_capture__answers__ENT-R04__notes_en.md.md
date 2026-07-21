---
title: "ENT-R04 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/ENT-R04/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "4248"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# ENT-R04 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/ENT-R04/notes_en|docs/experience_capture/answers/ENT-R04/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `4248` bytes

## خلاصه

This answer should be treated as: The execution system must preserve reason lineage after fill. Recommended flow: This prevents uncontrolled repeated entries from the same structural reason. 1. How exactly should "same reasons" be compared? 2. Is identical `reason_set_id` enough, or should similarity between reason sets also be measured? 3. If a new entry is based on overlapping but not identical reasons, is it allowed? 4. Can the same parent scenario create multiple positions if the entry reasons differ? 5. How should max-lot split positions be aggregated in reporting? 6. Should split child orders have separate stops/targets or shared logical management? 7. What exact event unlocks the reas

## Headings

- ENT-R04 — Notes and Open Questions
-   Classification
-   Core Hard Rules
-   Core Learnable Policies
-   Proposed Objects
-   Proposed Datasets
-   Proposed Fields
-   Proposed Labels
-   Proposed AI Modules
-   Architecture Consequence
-   Open Questions
-   Attachment Index

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/notes_en|DST-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/notes_en|ENT-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/notes_en|ENT-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/notes_en|EXE-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R02/notes_en|EXE-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/notes_en|EXT-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-06/notes_en|EXT-06 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-10/notes_en|EXT-10 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-12/notes_en|EXT-12 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
