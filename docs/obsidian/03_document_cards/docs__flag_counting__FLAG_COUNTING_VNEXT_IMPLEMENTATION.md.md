---
title: "Flag Counting vNext Implementation Notes"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4437"
entities:
  - "M0007"
  - "M0008"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting vNext Implementation Notes

**Source:** [[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4437` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document maps the v3 concept specification into the first clean MQL5 implementation module. Previous implementations evolved through patches over a pattern scanner. That architecture was not aligned with the final concept: Flag counting is fractal. Several sequences can be active in parallel. A confirmed F1 must spawn the search for F2. A confirmed F2 must spawn the search for F3. Different swing scales can produce different valid

## Headings

- Flag Counting vNext Implementation Notes
-   1. Why a vNext module exists
-   2. Data model
-   3. Node engine
-   4. F1 logic
-   5. F2 logic
-   6. F3 logic
-   7. Rendering
-   8. Inputs
-   9. Next work
-   Origin identity and live-root display contract

## Entities

`M0007`, `M0008`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[docs/releases/legacy_migration/general/b7d4f188eb79_README_FLAG_COUNTING_PHOENIX|EXP Flag Counting Phoenix]] — `experiment`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[mql5/Include/M0007/README_M0007_FlagCountingF1|M0007 — F1 Flag Counting MQL5 Module]] — `mql5_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
