---
title: "Flag Counting Implementation Checklist V2"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "10360"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting Implementation Checklist V2

**Source:** [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `10360` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This checklist converts `FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md` into concrete engineering tasks. Every item should be treated as an acceptance criterion for the next implementation pass. Recommended modules: Existing files may be reused, but the internal responsibilities should match these boundaries. [ ] Node extraction uses `high` and `low` only. [ ] No structure rule uses `open`. [ ] No structure rule uses `close`. [ ] No structure

## Headings

- Flag Counting Implementation Checklist V2
-   1. Module boundaries
-   2. Node engine checklist
-     2.1 High/low only
-     2.2 Raw node preservation
-     2.3 Alternating compressed view
-   3. ND detector checklist
-     3.1 ND node count
-     3.2 Adaptive L
-     3.3 50% cycle threshold
-   4. Flag geometry checklist
-     4.1 Common two-leg body

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|Flag Counting Sequence Contract V2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|Flag Counting Level 19 — State Gate and Dashboard Implementation Plan]] — `flag_counting_docs`
- [[docs/flag_counting/IMPLEMENTATION_LADDER_V1_INDEX|Flag Counting Implementation Ladder V1 Index]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|Flag Counting Implementation Checklist V4]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
