---
title: "Flag Counting Level 19 — Phase 27 Paper MFE / MAE Path Quality"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "3951"
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


# Flag Counting Level 19 — Phase 27 Paper MFE / MAE Path Quality

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `3951` bytes

## خلاصه

Phase 27 adds paper MFE / MAE path quality diagnostics above the Phase 26 Paper Performance Report. This phase still does **not** send real orders. It evaluates persistent paper trade lifecycle rows and produces close-only path quality metrics: Phase 27 writes: The State Gate snapshot now stores: Each row exports: Phase 27 is still close-only. It does **not** yet use intrabar high/low over the full path. So the values are deliberately named: The goal is not fake precision. The goal is to begin measuring path quality in a conservative, audit-friendly way. Examples: Examples: This phase supports the project objective of measuring path cleanliness, not only final outcome. It starts answering: E

## Headings

- Flag Counting Level 19 — Phase 27 Paper MFE / MAE Path Quality
-   Purpose
-   Hard safety contract
-   New CSV
-   New input
-   Snapshot-level fields
-   Row-level metrics
-   Important limitation
-   Buckets
-   Pullback pressure statuses
-   Why this matters
-   Execution safety

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
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY|Flag Counting Level 19 — Phase 23 Dry-Run Decision Policy]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|Flag Counting Level 19 — Phase 2 Closed-Bar Tracker]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
