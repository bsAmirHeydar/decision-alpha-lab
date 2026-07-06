---
title: "Flag Counting State Machine V3"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "10180"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting State Machine V3

**Source:** [[docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3|docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `10180` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document converts the sequence contract into a deterministic state machine. It is intended for implementation in MQL5 or any other detector backend. The state machine must operate on high/low nodes only. Every sequence has: A sequence never restarts at F1 after F1 has confirmed. The sequence advances in order. Use explicit statuses instead of implicit boolean flags. Display policy: Allowed entry points: 1. after ND/Hook, 2. after

## Headings

- Flag Counting State Machine V3
-   1. Global State Principles
-   2. Event Statuses
-   3. Sequence States
-     3.1 WAITING_FOR_F1
-     3.2 F1_BODY_LIVE
-     3.3 F1_POST_FLAG_CORRECTION
-     3.4 SEEKING_F2
-     3.5 F2_BODY_LIVE
-     3.6 F2_POST_FLAG_CORRECTION
-     3.7 SEEKING_F3
-     3.8 F3_BODY_LIVE

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
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
