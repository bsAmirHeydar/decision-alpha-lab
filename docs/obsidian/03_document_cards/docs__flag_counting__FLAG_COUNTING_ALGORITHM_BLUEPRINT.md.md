---
title: "Flag Counting Algorithm Blueprint"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "7207"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# Flag Counting Algorithm Blueprint

**Source:** [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `7207` bytes

## خلاصه

This document converts the concept specification into implementation-level algorithms. Fields: `int index` `datetime time` `double price` `int kind` where `+1 = high`, `-1 = low` `int scale_l` `bool confirmed` A lightweight copy of a node used inside a sequence: `index` `time` `price` `kind` `scale_l` `valid` Fields: `sequence_id` `parent_id` `root_id` `scale_l` `direction` `level`: F1/F2/F3 `phase`: F or ND `status`: live/confirmed/invalidated/terminal `position`: building_leg1, building_waist, building_leg2, waiting_internal1, waiting_internal2, waiting_rebreak, confirmed, terminal_f3 `origin` `leg1` `waist` `leg2` `internal1` `internal2` `confirm` `invalid` `branch_type`: none, normal_int

## Headings

- Flag Counting Algorithm Blueprint
-   1. Data model
-     FC_Node
-     FC_Point
-     FC_Sequence
-   2. Node engine
-   3. F1 body construction
-     Bullish F1 body
-     Bearish F1 body
-   4. F1 internal count
-     Bullish
-     Bearish

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|Flag Counting Concept Specification v2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|Flag Counting Level 19 — Phase 2 Closed-Bar Tracker]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION|Flag Counting Level 19 — Phase 3 Rally View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE5_PANEL_POLISH|Flag Counting Phoenix — Level 19 Phase 5 Panel Polish and Debug Usability]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
