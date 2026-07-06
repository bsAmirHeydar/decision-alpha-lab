---
title: "Flag Counting Level 19 — Phase 20A Compile Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20A_COMPILE_FIX.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "952"
concepts:
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting Level 19 — Phase 20A Compile Fix

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20A_COMPILE_FIX|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20A_COMPILE_FIX.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `952` bytes

## خلاصه

Phase 20A fixes a compile error introduced during Phase 20. The paper portfolio aggregate fields are snapshot-level fields, but their reset assignments were accidentally inserted into `FP_ResetStateGateTimeframeState`. `FP_StateGateTimeframeState` correctly does not own portfolio aggregate fields. Move the paper portfolio aggregate reset assignments to `FP_ResetStateGateSnapshot`. The fix keeps the Phase 20 portfolio aggregate model intact and only corrects the type ownership boundary. This fix does not change: It only fixes Phase 20 State Gate type reset ownership.

## Headings

- Flag Counting Level 19 — Phase 20A Compile Fix
-   Purpose
-   Error
-   Cause
-   Fix
-   Locked boundaries

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|Flag Counting Level 19 — Phase 10 Panel Line Debug Contract]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13A_COMPILE_FIX|Flag Counting Level 19 — Phase 13A Compile Fix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE17_PAPER_EXECUTION_LEDGER|Flag Counting Level 19 — Phase 17 Paper Execution / Dry Run Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING|Flag Counting Level 19 — Phase 18 Paper Ledger Lifecycle Tracking]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
