---
title: "Flag Counting Level 19 — Phase 23 Dry-Run Decision Policy"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "3657"
concepts:
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# Flag Counting Level 19 — Phase 23 Dry-Run Decision Policy

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `3657` bytes

## خلاصه

Phase 23 adds a dry-run decision policy above the Phase 22 Paper Filter Diagnostics layer. This phase still does **not** send real orders. It converts paper regime attribution and filter diagnostics into a policy gate that can allow or block a **dry-run only** decision. The policy can allow a dry-run row, but it never enables real execution. Phase 23 writes: Each State Gate timeframe state now stores: The State Gate snapshot now stores: Examples: The score is diagnostic and paper-only. It rewards: It penalizes: The score is capped to: Examples: Examples: Phase 23 is the first policy gate, but it is deliberately not an execution gate. It does not say: It only says whether a context is worth a

## Headings

- Flag Counting Level 19 — Phase 23 Dry-Run Decision Policy
-   Purpose
-   Hard safety contract
-   New CSV
-   New input
-   New per-timeframe fields
-   New snapshot-level fields
-   Policy names
-   Policy score
-   Policy block reasons
-   Policy status
-   Design boundary

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|Flag Counting Level 19 — Phase 10 Panel Line Debug Contract]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20_PAPER_PORTFOLIO_AGGREGATE_METRICS|Flag Counting Level 19 — Phase 20 Paper Portfolio / Aggregate Metrics]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|Flag Counting Level 19 — Phase 21 Paper Regime Attribution]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY|Flag Counting Level 19 — Phase 27 Paper MFE / MAE Path Quality]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|Flag Counting Level 19 — Phase 2 Closed-Bar Tracker]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
