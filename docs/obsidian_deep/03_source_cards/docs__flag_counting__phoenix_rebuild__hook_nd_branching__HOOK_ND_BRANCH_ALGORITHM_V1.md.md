
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1.md"
source_ext: ".md"
source_size: 11740
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Flag Counting", "Hook", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — HOOK_ND_BRANCH_ALGORITHM_V1.md

## Source

[[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1.md]]

## Summary

This document converts the Hook / ND branch-sequence contract into a deterministic implementation algorithm. The goal is to produce a list of Hook containers. Each Hook container can contain many branch sequences. Each branch sequence contains one to four counted same-side nodes after adaptive L normalization. A Hook qualifies… For each symbol, timeframe, direction side, and L: Node engine output must include: The high-side implementation is the mirror of low-side implementation. Important: increasing L requires rebuilding nodes and branches. Do not just remove extra branch nodes. For every possible active same-side node, including the latest pending node when enabled: The boundary itself is not counted as an internal branch number. Equality is ignored. Equality is not lower, higher, or a break. A Hook span can contain multiple internal branches. The algorithm uses right-to-left discover

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Hook / ND Branch Algorithm V1
  - 1. Goal
  - 2. Inputs
  - 3. Direction mapping
    - 3.1 Low-side Hook
    - 3.2 High-side Hook
  - 4. Main adaptive loop
  - 5. Building Hook contexts at one L
  - 6. Finding the origin boundary
    - 6.1 Low-side Hook
    - 6.2 High-side Hook
  - 7. Branch extraction model

## Related Source Documents

- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md]] — score `17`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `16`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `16`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/questions/remaining_v3_split/index_en|index_en.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
