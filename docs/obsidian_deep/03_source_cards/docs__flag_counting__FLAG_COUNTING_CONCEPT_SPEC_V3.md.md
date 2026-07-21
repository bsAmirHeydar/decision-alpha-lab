
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3.md"
source_ext: ".md"
source_size: 19577
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Flag Counting", "Hook", "Path Smoothness", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_CONCEPT_SPEC_V3.md

## Source

[[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> Status: authoritative design contract for the next Flag Counting implementation. This document replaces the earlier loose pattern-scanner interpretation. Flag Counting is not a collection of independent chart patterns. It is a fractal, multi-scale, multi-sequence movement grammar intended to partitio… The goal is to make the engine answer, programmatically and visually: Are we inside ND/Hook or inside an F-counting phase? If inside F-counting, which F-level are we in: F1, F2, F3? Which scale produced this sequence? Where are Origin, Leg1, Waist, Leg2, Internal 1, Internal 2, confirmation, and invalidation? Is the structure live, co

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Concept Specification v3
  - 1. Core worldview
  - 2. Why the earlier implementation failed
  - 3. Terms and definitions
    - 3.1 Node
    - 3.2 Scale L
    - 3.3 Direction
    - 3.4 Origin
    - 3.5 Leg1
    - 3.6 Waist
    - 3.7 Leg2
    - 3.8 Internal 1 and Internal 2

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `19`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/releases/legacy_migration/general/0b9f38e7e2fd_README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY|README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
