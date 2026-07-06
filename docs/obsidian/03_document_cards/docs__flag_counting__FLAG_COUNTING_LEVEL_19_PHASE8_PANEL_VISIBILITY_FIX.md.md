---
title: "Flag Counting Level 19 — Phase 8 Panel Visibility Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE8_PANEL_VISIBILITY_FIX.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "1817"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting Level 19 — Phase 8 Panel Visibility Fix

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE8_PANEL_VISIBILITY_FIX|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE8_PANEL_VISIBILITY_FIX.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `1817` bytes

## خلاصه

Phase 8 fixes the dashboard visibility issue observed on chart screenshots where only the small minimize buttons were visible and the panel body was not readable. The root cause is usually old saved EA inputs keeping a right-corner layout active while the new panel code expects a left-upper layout. In MetaTrader, saved input sets can persist even after defaults are changed in code. Phase 8 adds an explicit left-corner override: This input has priority over older right-corner settings. The corner priority is now: Default behavior: The panel background was also made more visible: body background changed from pure black to dark slate panel border and title border are brighter object z-order is

## Headings

- Flag Counting Level 19 — Phase 8 Panel Visibility Fix
-   Purpose
-   Fix
-   Visual improvements
-   Locked boundaries
-   What to check after applying

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE17_PAPER_EXECUTION_LEDGER|Flag Counting Level 19 — Phase 17 Paper Execution / Dry Run Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|Flag Counting Level 19 — Phase 22 Paper Filter Diagnostics]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|Flag Counting Level 19 — Phase 2 Closed-Bar Tracker]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
