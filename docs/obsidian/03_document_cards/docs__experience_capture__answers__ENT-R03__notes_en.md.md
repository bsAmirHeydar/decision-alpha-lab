---
title: "ENT-R03 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/ENT-R03/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "4164"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
  - "Validation"
---


# ENT-R03 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/ENT-R03/notes_en|docs/experience_capture/answers/ENT-R03/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `4164` bytes

## خلاصه

This answer should be treated as: The pending order engine should not keep orders alive only because they have not expired by time. It should re-check the reason set. Recommended flow: This should happen before any broker send or pending order maintenance. 1. Which reasons are core reasons versus secondary reasons? 2. Does any core reason failure cancel immediately? 3. Can a pending order remain alive if reasons are weakened but not invalidated? 4. Should weakened reasons move the order to `PENDING_LIMIT_REASON_WEAKENED`? 5. Is time expiration ever allowed as a secondary safety rule? 6. What exactly defines a missed limit? 7. Can a missed order remain eligible for replacement? 8. Should repl

## Headings

- ENT-R03 — Notes and Open Questions
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
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/notes_en|ENT-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/notes_en|EXE-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/notes_en|EXT-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-03/notes_en|EXT-03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-10/notes_en|EXT-10 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/notes_en|NDS-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/notes_en|RSK-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/notes_en|RSK-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/notes_en|SCN-R01 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
