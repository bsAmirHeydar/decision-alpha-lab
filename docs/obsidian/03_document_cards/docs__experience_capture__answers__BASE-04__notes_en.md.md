---
title: "BASE-04 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/BASE-04/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "2809"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
---


# BASE-04 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/BASE-04/notes_en|docs/experience_capture/answers/BASE-04/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `2809` bytes

## خلاصه

This experience should be treated as: Every future dataset, model, feature, label, and execution reason must pass an ontology filter. The system must not allow external concepts to enter silently. Gate states: Every future dataset should include a feature manifest. Each feature should declare: Future datasets should include an NDS ontology manifest: Possible columns: 1. Are spread, commission, and slippage allowed as execution-cost fields even though they are not market-anatomy concepts? 2. Is raw price allowed only as geometry, or can it become a feature directly? 3. Are volume/tick-volume fields forbidden by default? 4. Can session information ever be allowed if it is used only for executi

## Headings

- BASE-04 — Notes and Open Questions
-   Classification
-   Main Design Consequence
-   Proposed Ontology Gate
-   Proposed Feature Manifest Requirement
-   Proposed Forbidden Feature Families
-   Proposed Allowed Feature Families
-   Proposed Dataset Consequence
-   Proposed AI Modules
-   Open Questions
-   Architecture Consequence

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-02/notes_en|EXT-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-03/notes_en|EXT-03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-04/notes_en|EXT-04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/notes_en|NDS-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/notes_en|SCN-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/notes_en|DST-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/notes_en|ENT-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R02/notes_en|NDS-R02 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
