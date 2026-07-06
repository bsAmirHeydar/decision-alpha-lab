---
title: "EXE-R02 — Notes and Open Questions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/EXE-R02/notes_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "4175"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# EXE-R02 — Notes and Open Questions

**Source:** [[docs/experience_capture/answers/EXE-R02/notes_en|docs/experience_capture/answers/EXE-R02/notes_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `4175` bytes

## خلاصه

This answer should be treated as: Strictly speaking, this layer is not a learning layer. However, operational thresholds can be configured or empirically reviewed: These are execution configuration policies, not NDS ontology learning. This layer should not require AI for market reasoning. Possible non-reasoning modules: Broker validation should be built after ExecutionIntentCandidate but before any broker request. Recommended flow: If adjustment would change NDS structure, the validator should veto instead of silently modifying the trade. 1. Which broker constraints are mandatory in the first implementation? 2. What is the maximum allowed price normalization drift? 3. What is the maximum all

## Headings

- EXE-R02 — Notes and Open Questions
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
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
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
- [[docs/experience_capture/answers/EXT-01/notes_en|EXT-01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-06/notes_en|EXT-06 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-08/notes_en|EXT-08 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-10/notes_en|EXT-10 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-12/notes_en|EXT-12 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
