---
title: "SCN-R04 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/SCN-R04/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "4447"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# SCN-R04 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/SCN-R04/notes_en|docs/experience_capture/answers/SCN-R04/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `4447` bytes

## خلاصه

This answer should be treated as: The scenario engine should not recompute scenarios as anonymous fresh objects every time. It should preserve scenario identity and update its state. Recommended update flow: This creates an auditable scenario lifecycle. 1. Which constraints are core constraints versus secondary constraints? 2. What minimum constraint integrity score keeps a scenario alive? 3. How should partial constraint weakening be measured? 4. What exact condition triggers repricing? 5. Can a repriced scenario remain the same scenario if its zone changes completely? 6. How should relative weight be normalized across opposite directions? 7. How should weight update interact with risk budg

## Headings

- SCN-R04 — Notes and Open Questions
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
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/notes_en|ENT-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/notes_en|ENT-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/notes_en|ENT-R03 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/notes_en|EXE-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/notes_en|EXT-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-10/notes_en|EXT-10 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/notes_en|RSK-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/notes_en|RSK-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/notes_en|SCN-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
