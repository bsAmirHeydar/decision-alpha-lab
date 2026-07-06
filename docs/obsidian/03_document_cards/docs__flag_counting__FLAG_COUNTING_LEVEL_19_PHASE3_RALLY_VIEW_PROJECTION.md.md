---
title: "Flag Counting Level 19 — Phase 3 Rally View Projection"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "7399"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# Flag Counting Level 19 — Phase 3 Rally View Projection

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `7399` bytes

## خلاصه

Status: implemented design note Parent spec: `FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md` Parent implementation plan: `FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md` Phase 3 upgrades Level 19 State Gate from a closed-bar tracker into the first real anatomy projection layer. Phase 2 answered: Phase 3 now also answers: This is still not an entry engine. It does not answer: It only maps the locked Phoenix F1/F2/F3 output into a live multi-timeframe State Gate snapshot. Phase 3 does not change any locked anatomy logic. It does not edit or override: The new code only reads already-built Phoenix event fields. The direction is strictly: No reverse dependency is allowed. Phase 3

## Headings

- Flag Counting Level 19 — Phase 3 Rally View Projection
-   1. Purpose
-   2. Non-negotiable boundary
-   3. What Phase 3 adds
-   4. Rally View definition
-   5. Row selection
-   6. Latest established F
-   7. Probable next F
-   8. Body state labels
-   9. In-flag stage labels
-   10. Post-flag stage labels
-   11. CSV output

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|Flag Counting Level 19 — Multi-Timeframe State Gate and Dashboard Specification]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|Flag Counting Level 19 — State Gate and Dashboard Implementation Plan]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|Flag Counting Level 19 — Phase 2 Closed-Bar Tracker]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE5_PANEL_POLISH|Flag Counting Phoenix — Level 19 Phase 5 Panel Polish and Debug Usability]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
