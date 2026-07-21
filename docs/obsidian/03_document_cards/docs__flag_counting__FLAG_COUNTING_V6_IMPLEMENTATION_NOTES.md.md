---
title: "Flag Counting V6 Implementation Notes"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "10555"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting V6 Implementation Notes

**Source:** [[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `10555` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This patch adds a new implementation namespace: `FlagCountingV6`. V6 is not a patch over the old scanner. It is a modular implementation intended to follow the engineering documentation pack: 1. L-rule node extraction from candle highs/lows. 2. Equal high/low plateau merge. 3. Alternating node view per L. 4. Two-leg flag body construction. 5. F1/F2/F3 post-flag state evaluation. 6. Backfilled F2/F3 child origins from the parent post-fl

## Headings

- Flag Counting V6 Implementation Notes
-   Compile target
-   Important implementation choices
-     Node definition
-     Flag body
-     F1
-     F2
-     F3
-     ND / Hook
-     Renderer
-   Compile caveat
-   V6.1 semantic visibility and ownership repair

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES|Phoenix Implementation Notes]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|Flag Counting Level 19 — State Gate and Dashboard Implementation Plan]] — `flag_counting_docs`
- [[docs/flag_counting/IMPLEMENTATION_LADDER_V1_INDEX|Flag Counting Implementation Ladder V1 Index]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|Flag Counting Concept Specification v3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|Flag Counting Implementation Checklist V2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|Flag Counting Implementation Checklist V4]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
