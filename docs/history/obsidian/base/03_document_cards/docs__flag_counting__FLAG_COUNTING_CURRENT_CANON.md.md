---
title: "Flag Counting Current Canon"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "37939"
entities:
  - "M0007"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Flag Counting Current Canon

**Source:** [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `37939` bytes

## خلاصه

Status: **active source of truth for Phoenix implementation**. Scope: docs, code patches, audit, renderer, validation, and future execution modules related to Flag Counting. This document exists to remove decision drift. If any older Flag Counting document conflicts with this file, this file wins. The only active implementation path is Phoenix: Legacy paths are retained only as research history or reference material: Do not start new code from M0007, VNext, V6, old checklists, or old sequence contracts. Use the following hierarchy when implementing or auditing Phoenix: 1. **This file** — final decision source and conflict resolver. 2. `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md

## Headings

- Flag Counting Current Canon
-   1. Active implementation target
-   2. Canon hierarchy
-   3. Non-negotiable invariants
-   4. Final resolved decisions
-     4.1 Phase reset
-     4.2 F1 root preference
-     4.3 Fail-open
-     4.4 Main-chart visibility
-     4.5 High-L versus lower-L ownership
-     4.6 Pending nodes
-     4.7 Backfill window

## Entities

`M0007`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|Flag Counting Sequence Contract V4]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|Flag Counting Level 19 — State Gate and Dashboard Implementation Plan]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER|Flag Counting Level 19D — Closed-Bar Transition Event Ledger]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
