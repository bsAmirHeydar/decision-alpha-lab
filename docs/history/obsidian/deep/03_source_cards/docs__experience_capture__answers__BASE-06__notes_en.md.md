
---
type: source_card
source_path: "docs/experience_capture/answers/BASE-06/notes_en.md"
source_ext: ".md"
source_size: 3203
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Market Anatomy", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/BASE-06/notes_en|docs/experience_capture/answers/BASE-06/notes_en.md]]

## Summary

This experience should be treated as: The system must have two separated layers: Layer 1 is not trainable. Layer 2 is trainable. Every dataset should separate: This prevents AI outputs from being confused with NDS definitions. Every model should declare: Should the NDS concept registry be manually approved only? Should AI ever suggest new NDS concepts, or only new policy uses of existing concepts? How do we version Hook and Rally definitions if they ever evolve manually? Should model training fail automatically if forbidden features are present? Should all model outputs include a reason vector? Should every accepted AI result be explainable in NDS language? Should a model be allowed if it works only in one symbol but is NDS-compliant? Should niche models be accepted if their scope is explicitly declared? What is the minimum OOS evidence required before accepting a learnable policy? What

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- BASE-06 — Notes and Open Questions
  - Classification
  - Main Design Consequence
  - Proposed Layer Separation
    - Fixed Layer
    - Learnable Layer
  - Proposed Dataset Consequence
  - Proposed Model Manifest Requirement
  - Proposed AI Modules
  - Proposed Acceptance States
  - Open Questions
  - Architecture Consequence

## Related Source Documents

- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `17`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/architecture|architecture.md]] — score `16`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `16`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
