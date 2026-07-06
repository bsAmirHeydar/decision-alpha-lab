
---
type: source_card
source_path: "docs/experience_capture/answers/DST-R02/answer_normalized_en.md"
source_ext: ".md"
source_size: 5102
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Hook", "Rally", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/DST-R02/answer_normalized_en|docs/experience_capture/answers/DST-R02/answer_normalized_en.md]]

## Summary

Exit policy should be trained across multiple variants. The evaluation criteria for exit policy should remain aligned with the broader NDS principle: The system should not optimize exits only for comfort, win rate, or early certainty. It should evaluate how each exit policy affects the ability to keep profit open while reducing downside or realized opportunity loss. The user explicitly states: Therefore, the system should not hard-code a single exit method. It should compare families such as: But the preferred starting family is partial profit taking under different conditions, not trailing. Exit policies should be evaluated using the same core criteria already established for NDS opportunity selection: Suggested metrics: The best exit is not necessarily the one with highest win rate. The best exit is the one that preserves convex upside while controlling cost and protecting realized gai

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- DST-R02 — Normalized Interpretation
  - Core Claim
  - Exit Policy as Trainable
  - Evaluation Criteria
  - Trailing Stop Skepticism
  - Partial Close Preference
  - Multi-Condition Partial Exit
  - Keeping Profit Open
  - Cost of Exit Policy
  - Runner / Tail Logic
  - Machine-Readable Summary
  - Short Formal Statement

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/EXE-R01/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/EXT-02/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `10`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
