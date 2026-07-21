---
title: "NDS-R02 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/NDS-R02/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "5155"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# NDS-R02 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/NDS-R02/notes_en|docs/experience_capture/answers/NDS-R02/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `5155` bytes

## خلاصه

This answer should be treated as: The first implementation should separate deterministic construction from learnable scoring. Deterministic construction: Learnable scoring: 1. What exact node detector feeds the CycleHook builder at L2 and higher L values? 2. Should a node that appears in multiple sequences have multiple sequence roles or one canonical role plus references? 3. How should a sequence starter be defined when multiple nodes occur at nearly the same price? 4. Should strict lower/higher comparison use raw price or normalized point/tick value? 5. Should spread ever affect equality or strictness, or is sequence logic purely chart-price based? 6. What exact retracement formula should

## Headings

- NDS-R02 — Notes and Open Questions
-   Classification
-   Core Hard Rules
-   Core Flexible / Learnable Policies
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
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/notes_en|DST-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-04/notes_en|EXT-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/notes_en|NDS-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R03/notes_en|NDS-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/notes_en|SCN-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/notes_en|SCN-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/notes_en|BASE-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DATA-R03/notes_en|DATA-R03 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
