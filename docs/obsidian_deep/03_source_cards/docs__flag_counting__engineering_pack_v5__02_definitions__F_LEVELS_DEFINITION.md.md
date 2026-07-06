
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION.md"
source_ext: ".md"
source_size: 4266
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — F_LEVELS_DEFINITION.md

## Source

[[docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION|docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION.md]]

## Summary

F1, F2, and F3 all use the same body geometry: Their differences are sequence role and post-body requirements. F1 is the first flag in a sequence. F1 must start from a valid phase boundary: terminal extreme of ND/Hook; end of opposite sequence; confirmed opposite F1 that locks previous F3 and starts a new opposite sequence; another explicitly owned phase boundary. F1 must not start from the middle of an active movement just because a local alternating window exists. F1 appears on chart after the probable two-leg body has been hit/completed. Before Leg2, it is only a seed and should not appear as F1 body on main chart. F1 confirms when: Bullish F1 confirms with: Bearish F1 confirms with: Before confirmation: Bullish: Bearish: F2 is the second flag in a sequence. F2 is authorized only after F1 confirms. However, F2 origin is backfilled from the F1 post-flag correction context. Bullish: Bea

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- F-Level Definitions
  - Shared Body
  - F1 Definition
    - F1 Start
    - F1 Display
    - F1 Confirmation
    - F1 Invalidation
  - F2 Definition
    - F2 Authorization
    - F2 Origin
    - F2 Size
    - F2 Invalidation

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `10`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-06/notes_en|notes_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
