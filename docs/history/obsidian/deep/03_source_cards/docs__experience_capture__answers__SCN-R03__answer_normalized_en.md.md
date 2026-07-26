
---
type: source_card
source_path: "docs/experience_capture/answers/SCN-R03/answer_normalized_en.md"
source_ext: ".md"
source_size: 6871
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/SCN-R03/answer_normalized_en|docs/experience_capture/answers/SCN-R03/answer_normalized_en.md]]

## Summary

Scenario ranking in NDS is not a truth-selection problem. The system should not force one scenario to become dominant unless the structure itself requires it. The correct model is: Multiple scenarios can remain alive at the same time if each has its own NDS evidence and offers a convex opportunity. The goal is not to predict which scenario is correct. The goal is to find which scenario offers: A scenario does not need to become the only dominant scenario. Instead: A bullish scenario and bearish scenario may both remain alive as conditional plans if both have valid NDS constraints and both offer favorable convexity at their own zones. The user explicitly states: This changes the ranking objective. The model should not rank scenarios by "which one is most likely true" first. It should rank by: Correctness is secondary. Payoff shape is primary. A convex trade in this context means: Suggeste

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- SCN-R03 — Normalized Interpretation
  - Core Claim
  - Scenario Does Not Need to Dominate
  - Potential Over Correctness
  - Convex Trade Definition
  - Scenario Threads
  - Ranking Objective
  - Win Rate Comes After Convexity
  - Continuous Testing
  - Multi-Zone Selection
  - Veto Logic
  - Risk Allocation

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/SCN-R03|SCN-R03.md]] — score `12`
- [[docs/experience_capture/answers/SCN-R03/notes_en|notes_en.md]] — score `9`
- [[docs/experience_capture/answers/SCN-R03/question_en|question_en.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `8`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `8`
- [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] — score `8`
- [[docs/debug/E0006/README|README.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
