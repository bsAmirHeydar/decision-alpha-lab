---
title: "ENT-R02 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/ENT-R02/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "4175"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# ENT-R02 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/ENT-R02/notes_en|docs/experience_capture/answers/ENT-R02/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `4175` bytes

## خلاصه

This answer should be treated as: ENT-R02 should not directly execute trades. It should create an `ExecutionIntent`. Recommended flow: This preserves the no-send architecture. 1. Should the stop buffer be trained globally first or per symbol/timeframe? 2. What candidate buffer values should be tested first? 3. Should buffer be measured in points, spread multiples, or node-distance percentage? 4. Can the buffer ever move the stop so far that the trade loses convexity? 5. What is the maximum allowed buffer before entry is vetoed? 6. Should buy limit stop and take profit also have any spread adjustment, or only entry? 7. For sell limit, should entry price ever be spread-adjusted, or only stop l

## Headings

- ENT-R02 — Notes and Open Questions
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
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/notes_en|ENT-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/notes_en|EXE-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/notes_en|EXT-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-10/notes_en|EXT-10 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/notes_en|RSK-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/notes_en|RSK-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/notes_en|SCN-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R04/notes_en|SCN-R04 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
