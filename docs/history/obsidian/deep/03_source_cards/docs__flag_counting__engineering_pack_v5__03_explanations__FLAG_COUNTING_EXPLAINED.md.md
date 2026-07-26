
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/03_explanations/FLAG_COUNTING_EXPLAINED.md"
source_ext: ".md"
source_size: 2157
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Flag Counting", "Hook", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_EXPLAINED.md

## Source

[[docs/flag_counting/engineering_pack_v5/03_explanations/FLAG_COUNTING_EXPLAINED|docs/flag_counting/engineering_pack_v5/03_explanations/FLAG_COUNTING_EXPLAINED.md]]

## Summary

Flag Counting treats movement as a sequence of owned two-leg structures, where each structure must have a legitimate origin, phase context, lifecycle role, and post-body behavior. A sliding-window detector sees any local alternating pattern: and may call it a bullish flag. This is wrong because it cannot answer: Why did the flag start there? Which sequence owns it? Is it F1, F2, or F3? Is it inside a larger active chain? Did it begin from ND, opposite sequence end, or arbitrary mid-move noise? What invalidates it? What does it produce next? This caused orphan lines that started from the middle of moves. A sequence chain begins at a phase boundary. The engine is not allowed to restart F1 at every local opportunity. After F1 confirms, the system searches for F2 in the same chain. After F2 confirms, the system searches for F3. F3 terminates the chain. The model tries to avoid idle movement.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Explained
  - The Model in One Sentence
  - Why Sliding Windows Failed
  - Sequence-Based Interpretation
  - Why Every Movement Should Belong Somewhere
  - The Difference Between Logic and Rendering
  - What Makes a Flag Real

## Related Source Documents

- [[docs/flag_counting/engineering_pack_v5/03_explanations/ANTI_PATTERNS_AND_FAILURES|ANTI_PATTERNS_AND_FAILURES.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA.md]] — score `8`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `8`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
