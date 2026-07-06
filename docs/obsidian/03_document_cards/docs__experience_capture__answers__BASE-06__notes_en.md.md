---
title: "BASE-06 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/BASE-06/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "3203"
concepts:
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
---


# BASE-06 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/BASE-06/notes_en|docs/experience_capture/answers/BASE-06/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `3203` bytes

## خلاصه

This experience should be treated as: The system must have two separated layers: Layer 1 is not trainable. Layer 2 is trainable. Every dataset should separate: This prevents AI outputs from being confused with NDS definitions. Every model should declare: 1. Should the NDS concept registry be manually approved only? 2. Should AI ever suggest new NDS concepts, or only new policy uses of existing concepts? 3. How do we version Hook and Rally definitions if they ever evolve manually? 4. Should model training fail automatically if forbidden features are present? 5. Should all model outputs include a reason vector? 6. Should every accepted AI result be explainable in NDS language? 7. Should a mode

## Headings

- BASE-06 — Notes and Open Questions
-   Classification
-   Main Design Consequence
-   Proposed Layer Separation
-     Fixed Layer
-     Learnable Layer
-   Proposed Dataset Consequence
-   Proposed Model Manifest Requirement
-   Proposed AI Modules
-   Proposed Acceptance States
-   Open Questions
-   Architecture Consequence

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[docs/experience_capture/answers/BASE-03/notes_en|BASE-03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/notes_en|NDS-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-01/notes_en|BASE-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/notes_en|BASE-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/notes_en|BASE-05 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-02/notes_en|EXT-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-03/notes_en|EXT-03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-04/notes_en|EXT-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/notes_en|SCN-R01 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
