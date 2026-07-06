
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS.md"
source_ext: ".md"
source_size: 3979
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — F1_F2_F3_ALGORITHMS.md

## Source

[[docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS|docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS.md]]

## Summary

After Leg2: Bullish deepest adverse: Bearish deepest adverse: If no valid internal 1/2 exists and price passes Leg2 again: Before confirmation: Only after F1 confirmed. Use FlagBodyBuilder from F2 origin. F2 seed may be shown. Then: If after F2 body the correction passes F2 Waist but not F2 Origin: Continue branch logic into 3/4 if present. Only after F2 confirmed. Backfill Origin into the F2 correction window, force Leg1 to the F2 confirmation node, then use normal FlagBodyBuilder rules for Waist and Leg2 after F2 confirmation. F3 seed/leg development may be shown, but incomplete bodies cannot be terminal. If `condA OR condB`: Else: After completion: For child flags F2 and F3, only the child Origin is allowed to be backfilled into the unfinished parent correction/hit window. The child Leg1 is the parent confirmation hit itself. Child Waist and Leg2 are built only aft… For F3 specificall

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- F1 / F2 / F3 Algorithms
  - F1 Algorithm
    - Create F1
    - Show F1
    - Track Post-F1 Context
    - F1 Extension
    - F1 Invalidation
    - F1 Confirmation
  - F2 Algorithm
    - Authorize F2
    - Build F2
    - F2 Qualification

## Related Source Documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/DEDUP_AUDIT_ALGORITHM|DEDUP_AUDIT_ALGORITHM.md]] — score `11`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|MODULE_ARCHITECTURE.md]] — score `11`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|NODE_ENGINE_ALGORITHM.md]] — score `11`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|README.md]] — score `11`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `10`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
