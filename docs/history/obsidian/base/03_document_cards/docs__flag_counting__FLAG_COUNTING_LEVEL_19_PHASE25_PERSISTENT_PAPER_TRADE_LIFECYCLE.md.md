---
title: "Flag Counting Level 19 — Phase 25 Persistent Paper Trade Lifecycle Engine"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25_PERSISTENT_PAPER_TRADE_LIFECYCLE.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4428"
concepts:
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting Level 19 — Phase 25 Persistent Paper Trade Lifecycle Engine

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25_PERSISTENT_PAPER_TRADE_LIFECYCLE|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25_PERSISTENT_PAPER_TRADE_LIFECYCLE.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4428` bytes

## خلاصه

Phase 25 adds a lifecycle engine above the Phase 24 Persistent Paper Trade Ledger. This phase still does **not** send real orders. It takes persistent paper trade rows and evaluates their current paper lifecycle using the latest closed candle close only. Phase 25 writes: Each State Gate timeframe state now stores: The snapshot now stores: Phase 25 can classify persistent paper trades as: Phase 25 remains close-only: It does not use intrabar high/low yet. For BUY-like paper trade directions: For SELL-like paper trade directions: When a non-zero invalidation distance exists, the engine computes: If invalidation distance is unavailable, R stays pending. Every Phase 25 row keeps: No order is ope

## Headings

- Flag Counting Level 19 — Phase 25 Persistent Paper Trade Lifecycle Engine
-   Purpose
-   Hard safety contract
-   New CSV
-   New input
-   New per-timeframe fields
-   Snapshot aggregate fields
-   Lifecycle states
-   Terminal states
-   Path states
-   Evaluation method
-   R-equivalent

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|Flag Counting Level 19 — Phase 10 Panel Line Debug Contract]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE17_PAPER_EXECUTION_LEDGER|Flag Counting Level 19 — Phase 17 Paper Execution / Dry Run Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING|Flag Counting Level 19 — Phase 18 Paper Ledger Lifecycle Tracking]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS|Flag Counting Level 19 — Phase 19 Paper Result Metrics / R-Equivalent Summary]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
