---
title: "Flag Counting Implementation Checklist V4"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "5397"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting Implementation Checklist V4

**Source:** [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `5397` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> Use this checklist before modifying code. [ ] Reuse the existing project node engine. [ ] Do not redefine L inside FlagCounting. [ ] L means minimum left/right candles that do not reach the candidate high/low price. [ ] Equal highs/lows are merged as one plateau node according to existing logic. [ ] Equality does not count as break. [ ] Nodes do not expire after confirmation. Each node must expose: [ ] time [ ] price [ ] type: high/low

## Headings

- Flag Counting Implementation Checklist V4
-   1. Node Engine
-   2. Data Model
-   3. F1 Checklist
-   4. F2 Checklist
-   5. F3 Checklist
-   6. Hook/ND Checklist
-   7. Boundary Checklist
-   8. Display Checklist
-   9. Anti-Regression Tests

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|Flag Counting Phoenix — Level 19 Phase 6 State Contract Storage]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|Flag Counting Level 19 — State Gate and Dashboard Implementation Plan]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|Flag Counting Sequence Contract V2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|Flag Counting Sequence Contract V3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|Flag Counting Sequence Contract V4]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_VISUALIZATION_SPEC|Flag Counting Visualization Specification]] — `flag_counting_docs`
- [[docs/flag_counting/IMPLEMENTATION_LADDER_V1_INDEX|Flag Counting Implementation Ladder V1 Index]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
