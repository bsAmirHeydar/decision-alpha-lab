---
title: "Flag Counting Sequence Contract V4"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "23682"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# Flag Counting Sequence Contract V4

**Source:** [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `23682` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file remains the active semantic sequence contract for Phoenix, but it is subordinate to: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document is the canonical English contract for the Flag Counting experiment. It replaces the earlier loose/sliding-window interpretation with a sequence-based, high/low-node-only state machine. The goal of this contract is not to make the chart visually pleasing by approximation. The goal is to define the exact logical object that the code must detect, persist, invalidate, confirm, render, and audit. The entire system is based on **high/low node

## Headings

- Flag Counting Sequence Contract V4
-   1. Core Principle
-   2. Node Definition
-   3. Equality, Hit, Break, and Pass
-   4. Flag Body Definition
-   5. Leg1 and Waist Updating
-   6. The Three F Levels
-   7. Sequence Ownership
-   8. F1 Start
-   9. F1 Body and Display Maturity
-   10. F1 Post-Flag Logic
-   11. F1 Leg2 Extension Rule

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
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
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|Flag Counting Algorithm Blueprint]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|Flag Counting Concept Specification v2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|Flag Counting Concept Specification v3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|Flag Counting Implementation Checklist V4]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
