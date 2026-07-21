---
title: "Flag Counting State Machine V4"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V4.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4798"
concepts:
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
---


# Flag Counting State Machine V4

**Source:** [[docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V4|docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V4.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4798` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document converts the sequence contract into implementation states. The state machine is sequence-based. It is not a sliding-window detector. A directional chain has the following high-level states: The engine waits for a legal F1 start context: terminal ND/Hook extreme; end/lock of opposite sequence; first confirmed opposite F1 that locks a previous F3. No arbitrary mid-move F1 is allowed. The engine builds a two-leg F1 candidate

## Headings

- Flag Counting State Machine V4
-   1. Main Chain State
-   2. WAIT_PHASE_BOUNDARY
-   3. BUILD_F1_BODY
-   4. F1_POST_FLAG_COUNTING
-   5. F1_CONFIRMED_BUILD_F2
-   6. F2_BODY_OR_SEED
-   7. F2_POST_FLAG_COUNTING
-   8. F2_CONFIRMED_BUILD_F3
-   9. F3_BODY_OR_SEED
-   10. F3_COMPLETED_EXTENSION
-   11. F3_LOCKED_CHAIN_DONE

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|Flag Counting Algorithm Blueprint]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|Flag Counting Concept Specification v2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|Flag Counting Concept Specification v3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_GLOSSARY|Flag Counting Glossary]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|Flag Counting Implementation Checklist V3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|Flag Counting Implementation Checklist V4]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|Flag Counting Level 19 — Phase 10 Panel Line Debug Contract]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
