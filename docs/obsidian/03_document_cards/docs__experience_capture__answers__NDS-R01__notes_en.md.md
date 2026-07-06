---
title: "NDS-R01 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/NDS-R01/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "3656"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
  - "Validation"
---


# NDS-R01 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/NDS-R01/notes_en|docs/experience_capture/answers/NDS-R01/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `3656` bytes

## خلاصه

This answer should be treated as: The system should not feed AI raw candle data as the primary representation. The system should first construct NDS-native objects: AI should operate on this packet. 1. Should X-axis and Y-axis be stored as separate tables or inside one state packet? 2. What exact numeric rule defines Hook 1/2/3 symmetry? 3. What exact numeric rule defines Hook 4 extension beyond symmetry? 4. Should F2 >= F1 be measured by price distance, time, or both? 5. Should F symmetry include both size and duration? 6. How should parent timeframe dominance be scored when parent and child conflict? 7. Should lower timeframe ever veto higher timeframe, or only refine entry? 8. How should

## Headings

- NDS-R01 — Notes and Open Questions
-   Classification
-   Core Hard Rules
-   Proposed Canonical Objects
-   Proposed Datasets
-   Proposed Fields for `canonical_state_packet_v1`
-   Proposed Labels
-   Proposed AI Modules
-   Architecture Consequence
-   Open Questions
-   Attachment Index

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/notes_en|SCN-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/notes_en|DST-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/notes_en|ENT-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-03/notes_en|EXT-03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-04/notes_en|EXT-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R03/notes_en|NDS-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/notes_en|SCN-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/notes_en|BASE-04 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
