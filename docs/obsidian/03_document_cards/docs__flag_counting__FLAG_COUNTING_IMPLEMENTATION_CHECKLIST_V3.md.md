---
title: "Flag Counting Implementation Checklist V3"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "8148"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting Implementation Checklist V3

**Source:** [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `8148` bytes

## خلاصه

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This checklist is for implementing or auditing the Flag Counting V3 contract. Each item should be reviewed before touching detector code. [ ] Detector reads swing high / swing low nodes. [ ] F logic does not use candle open. [ ] F logic does not use candle close. [ ] F logic does not use candle body. [ ] F logic does not use candle color. [ ] ND logic does not use candle open. [ ] ND logic does not use candle close. [ ] ND logic does n

## Headings

- Flag Counting Implementation Checklist V3
-   1. High/Low Only
-   2. Raw Node Preservation
-   3. Flag Body Builder
-   4. F1
-   5. F2
-   6. F3
-   7. ND / Hook
-   8. Rendering
-   9. Duplicate Handling
-   10. Audit Logging
-   11. Anti-Regression Tests

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|Flag Counting Algorithm Blueprint]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|Flag Counting Concept Specification v2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|Flag Counting Concept Specification v3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_GLOSSARY|Flag Counting Glossary]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|Flag Counting Implementation Checklist V4]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
