---
title: "Flag Counting Level 19 — Phase 25B Responsive Panel Layout"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25B_RESPONSIVE_PANEL_LAYOUT.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "1459"
concepts:
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Rally"
---


# Flag Counting Level 19 — Phase 25B Responsive Panel Layout

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25B_RESPONSIVE_PANEL_LAYOUT|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25B_RESPONSIVE_PANEL_LAYOUT.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `1459` bytes

## خلاصه

This patch redesigns the State Gate panel layout so it adapts better to different chart resolutions and monitor sizes. The panel now reads the chart pixel width and height at runtime. Width is chosen responsively instead of staying fixed. Font size and row height are reduced automatically on smaller charts. The panel position is clamped inside the visible chart area. The content switches between roomy, compact, and ultra-compact rendering modes. Rally and Hook preview rows are reduced automatically on smaller screens. Section buttons remain intact: main minimize button per-timeframe collapse button Rally collapse button Hook collapse button Keep the dashboard readable on: lower-resolution mo

## Headings

- Flag Counting Level 19 — Phase 25B Responsive Panel Layout
-   What changed
-   Goal
-   Rendering modes
-   Safety

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|Flag Counting Algorithm Blueprint]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|Flag Counting Concept Specification v2]] — `flag_counting_docs`
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

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
