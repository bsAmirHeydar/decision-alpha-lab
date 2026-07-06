
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/02_definitions/STATUS_AND_LIFECYCLE_DEFINITION.md"
source_ext: ".md"
source_size: 2603
empty: false
generated_at: 2026-07-06
concepts: ["Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — STATUS_AND_LIFECYCLE_DEFINITION.md

## Source

[[docs/flag_counting/engineering_pack_v5/02_definitions/STATUS_AND_LIFECYCLE_DEFINITION|docs/flag_counting/engineering_pack_v5/02_definitions/STATUS_AND_LIFECYCLE_DEFINITION.md]]

## Summary

A partial structure that has not yet formed a complete body. F1 seed is hidden on main chart. F2/F3 seed may be displayed because it belongs to an existing confirmed parent context and helps debug stage progression. A possible body under construction. May have Origin/Leg1/Waist but no Leg2 yet. A complete two-leg body exists. For F1, this is the earliest display stage. The body exists and the engine is tracking post-flag internal numbering. This is where 1/2/3/4 and ND/Hook may appear. A child F object has a body but is waiting for size/scale qualification. F2 may wait for: F3 may wait for either OR condition: F1 or F2 only. F1 confirms after post-flag internal numbering and Leg2 re-pass without Waist invalidation. F2 confirms after internal numbering or waist-break branch and Leg2 re-pass without Origin invalidation. F3 only. F3 completes after body plus qualification. It does not requi

## Concepts

[[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Status and Lifecycle Definition
  - Recommended Status Enum
  - SEED
  - BODY_CANDIDATE
  - LIVE_BODY
  - POST_FLAG_COUNTING
  - QUALIFYING
  - CONFIRMED
  - COMPLETED
  - EXTENDING
  - LOCKED
  - INVALIDATED

## Related Source Documents

- [[docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION|F_LEVELS_DEFINITION.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA.md]] — score `8`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `8`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-02/answer_raw_en|answer_raw_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-03/answer_normalized_en|answer_normalized_en.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
