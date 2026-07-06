---
title: "Flag Counting Level 19 — Phase 9 Visual Debug Contract"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "3736"
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


# Flag Counting Level 19 — Phase 9 Visual Debug Contract

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `3736` bytes

## خلاصه

Phase 9 turns the State Gate panel and CSV exports into a stronger debug contract. The previous phases built: closed-bar timeframe tracking Rally View projection Hook View projection panel usability State Contract storage left-upper panel forcing Phase 9 does not add entry logic. It makes the existing State Gate easier to verify after compile and easier to debug on a live chart. Level 19 remains a read-only projection layer. It reads the locked anatomy outputs and exposes them as: It must not mutate the anatomy engines. Phase 9 does not change: These are diagnostic-only switches. When enabled, the dashboard shows a diagnostics line near the top: This line exists for two reasons: 1. to make t

## Headings

- Flag Counting Level 19 — Phase 9 Visual Debug Contract
-   Purpose
-   Core principle
-   Locked engines
-   New inputs
-   Panel diagnostics line
-   Effective corner priority
-   Diagnostics CSV
-   Manifest additions
-   Acceptance checklist
-   If the panel is still invisible
-   Status

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
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
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY|Flag Counting Level 19 — Phase 27 Paper MFE / MAE Path Quality]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
