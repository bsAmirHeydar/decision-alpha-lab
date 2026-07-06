---
title: "EXE-R02 — Normalized Interpretation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/EXE-R02/answer_normalized_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "4123"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
  - "Validation"
---


# EXE-R02 — Normalized Interpretation

**Source:** [[docs/experience_capture/answers/EXE-R02/answer_normalized_en|docs/experience_capture/answers/EXE-R02/answer_normalized_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `4123` bytes

## خلاصه

Broker validation and send-gate rules are mechanical. They are not part of the native NDS decision ontology. Their rules are clear and deterministic. Recommended canonical rule: The broker validator should not reinterpret the market, rank scenarios, select zones, or change NDS structural reasoning. It should only check whether an already-created ExecutionIntent is mechanically valid for broker submission. NDS responsibility: Broker Validator responsibility: The validator is not an AI policy layer. It is not a scenario layer. It is not a zone layer. It is not an entry-selection layer. It is a mechanical send gate. The broker validator should handle deterministic broker-side constraints such a

## Headings

- EXE-R02 — Normalized Interpretation
-   Core Claim
-   Separation of Responsibilities
-   Deterministic Constraint Layer
-   Mechanical Adjust vs Veto
-   No NDS Reasoning Mutation
-   Audit Requirement
-   Send Gate
-   Machine-Readable Summary
-   Short Formal Statement

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|BASE-05 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|DST-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/answer_normalized_en|ENT-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/answer_normalized_en|EXE-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-06/answer_normalized_en|EXT-06 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-07/answer_normalized_en|EXT-07 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R03/answer_normalized_en|NDS-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/answer_normalized_en|RSK-R02 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
