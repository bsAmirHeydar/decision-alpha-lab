---
title: "Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "7873"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `7873` bytes

## خلاصه

Phase 4 extends the Level 19 State Gate from a closed-bar tracker plus Rally View projection into a full two-sided anatomy gate: Rally View reads the existing F1/F2/F3 anatomy. Hook View reads the existing Hook/ND branch anatomy. The dashboard displays both views per configured timeframe. The CSV export stores both Rally rows and Hook rows. This phase is still read-only. It does not create, modify, filter, or reinterpret the locked Node, Hook/ND, Flag Body, Internal Count, F1, F2, or F3 engines. The following layers remain locked and unchanged: Phase 4 only runs the existing Phoenix anatomy pipeline per configured State Gate timeframe and projects the resulting `FP_HookBranch` rows into `FP_

## Headings

- Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection
-   Purpose
-   Hard boundary
-   Conceptual meaning
-   Timeframe model
-   Hook View source
-   Projectable Hook rows
-   Sorting and display priority
-   Hook polarity
-   Current node state
-   Latest high and low node inside the Hook row
-   Dashboard behavior

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|Flag Counting Level 19 — State Gate and Dashboard Implementation Plan]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|Flag Counting Level 19 — Phase 2 Closed-Bar Tracker]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|Flag Counting Phoenix — Level 19 Phase 6 State Contract Storage]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|Flag Counting Level 19 — Phase 7 Left-Upper Panel and Section Toggles]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
