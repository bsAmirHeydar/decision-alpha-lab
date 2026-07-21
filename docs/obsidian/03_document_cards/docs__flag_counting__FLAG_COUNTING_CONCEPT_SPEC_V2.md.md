---
title: "Flag Counting Concept Specification v2"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "17078"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
  - "Validation"
---


# Flag Counting Concept Specification v2

**Source:** [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `17078` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> Status: concept contract, not implementation. Language: English. Purpose: freeze the full F-counting logic before any new code is written. This document converts the latest discussion into an engineering contract for the next implementation of the Flag Counting experiment. The key correction is that Flag Counting is not a loose pattern scanner. It is a fractal, multi-scale, multi-sequence market-state system. The market movement should

## Headings

- Flag Counting Concept Specification v2
-   1. Core thesis
-   2. Terminology
-     2.1 Node
-     2.2 Scale `L`
-     2.3 Sequence
-     2.4 F body
-     2.5 Body size
-   3. F1 contract
-     3.1 F1 body
-     3.2 F1 internal 1 and 2
-     3.3 F1 requires internal 1 and 2 before confirmation

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|Flag Counting Sequence Contract V3]] — `flag_counting_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|Flag Counting Algorithm Blueprint]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|Flag Counting Level 19 — Phase 28 Context Performance Matrix]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
