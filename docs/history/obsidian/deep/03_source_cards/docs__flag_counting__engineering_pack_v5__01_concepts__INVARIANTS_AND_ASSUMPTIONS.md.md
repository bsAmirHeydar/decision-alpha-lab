
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/01_concepts/INVARIANTS_AND_ASSUMPTIONS.md"
source_ext: ".md"
source_size: 3628
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React"]
entities: []
---

# Source Card — INVARIANTS_AND_ASSUMPTIONS.md

## Source

[[docs/flag_counting/engineering_pack_v5/01_concepts/INVARIANTS_AND_ASSUMPTIONS|docs/flag_counting/engineering_pack_v5/01_concepts/INVARIANTS_AND_ASSUMPTIONS.md]]

## Summary

This file lists rules that must remain true in all implementations. Only candle highs and lows feed structural logic. Node extraction is delegated to the existing project node module. Open, close, body, candle color, and candle direction do not participate in F or ND decisions. A node does not expire. Equality is not a break. A boundary must be passed with strict inequality. A flag is always two legs: A body without Leg2 is not a complete flag body. Leg1 is the true extreme before correction, not the first small node. Waist is the true adverse correction extreme before Leg2. Waist must update while correction deepens/higher-corrects. In bullish body, correction must not pass origin. In bearish body, correction must not pass origin. In a chain, order is F1 -> F2 -> F3. After F1 confirms, search for F2 in the same chain. After F2 confirms, search for F3 in the same chain. Do not start arbi

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Invariants and Assumptions
  - Structural Input Invariants
  - Flag Geometry Invariants
  - Sequence Invariants
  - F1 Invariants
  - F2 Invariants
  - F3 Invariants
  - Hook / ND Invariants
  - Rendering Invariants

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/ai_execution/README|README.md]] — score `12`
- [[docs/debug/E0008/README|README.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
