---
title: "ENT-R04 — Normalized Interpretation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/ENT-R04/answer_normalized_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "6011"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# ENT-R04 — Normalized Interpretation

**Source:** [[docs/experience_capture/answers/ENT-R04/answer_normalized_en|docs/experience_capture/answers/ENT-R04/answer_normalized_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `6011` bytes

## خلاصه

After a limit entry is filled, the reason set that created the trade must become locked to the active position. As long as that position remains open, the system must not open a duplicate trade using the same reasons. Recommended canonical rule: This creates a `PositionReasonLock`. Before fill, the system has: After fill, the filled intent becomes: The scenario does not necessarily disappear. It can remain as the parent analytical object, but the active risk and trade management should move into a position object. Suggested relationship: The `PositionThread` should preserve lineage: The most important rule in this answer is: This prevents repeated entries from the same structural logic while

## Headings

- ENT-R04 — Normalized Interpretation
-   Core Claim
-   Scenario-to-Position Transition
-   Duplicate Trade Block
-   Same Reasons vs New Reasons
-   PositionThread
-   Multi-Exit Logic
-   Hedge Separation
-   Opposite Scenario Handling
-   Split Orders and Logical Position
-   Position Completion
-   Machine-Readable Summary

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|BASE-05 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DATA-R03/answer_normalized_en|DATA-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|DST-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/answer_normalized_en|ENT-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/answer_normalized_en|ENT-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/answer_normalized_en|ENT-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/answer_normalized_en|EXE-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R02/answer_normalized_en|EXE-R02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-06/answer_normalized_en|EXT-06 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
