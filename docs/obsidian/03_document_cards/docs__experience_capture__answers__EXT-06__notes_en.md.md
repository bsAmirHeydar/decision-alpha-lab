---
title: "EXT-06 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/EXT-06/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "3272"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# EXT-06 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/EXT-06/notes_en|docs/experience_capture/answers/EXT-06/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `3272` bytes

## خلاصه

This experience should be treated as: This rule should live in a deterministic gate before AI policy. Suggested gate: Possible outputs: 1. Does "one point beyond the node" refer to bid/ask, mid, candle wick, or chart price? 2. For buy entries, should penetration be evaluated using bid or ask? 3. For sell entries, should penetration be evaluated using bid or ask? 4. Should the system store raw chart penetration separately from executable broker stop penetration? 5. Does spread affect structural penetration or only execution stop placement? 6. Can a new Extreme be created immediately after penetration if a new NDS structure forms? 7. Should penetration-then-reversal be used to widen future Ext

## Headings

- EXT-06 — Notes and Open Questions
-   Classification
-   Proposed Hard Rule
-   Proposed States
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
- [[docs/experience_capture/answers/ENT-R04/notes_en|ENT-R04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/notes_en|EXE-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R02/notes_en|EXE-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/notes_en|EXT-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-10/notes_en|EXT-10 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-12/notes_en|EXT-12 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
