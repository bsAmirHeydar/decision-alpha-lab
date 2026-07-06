
---
type: source_card
source_path: "docs/experience_capture/answers/ENT-R04/answer_normalized_en.md"
source_ext: ".md"
source_size: 6011
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/ENT-R04/answer_normalized_en|docs/experience_capture/answers/ENT-R04/answer_normalized_en.md]]

## Summary

After a limit entry is filled, the reason set that created the trade must become locked to the active position. As long as that position remains open, the system must not open a duplicate trade using the same reasons. Recommended canonical rule: This creates a `PositionReasonLock`. Before fill, the system has: After fill, the filled intent becomes: The scenario does not necessarily disappear. It can remain as the parent analytical object, but the active risk and trade management should move into a position object. Suggested relationship: The `PositionThread` should preserve lineage: The most important rule in this answer is: This prevents repeated entries from the same structural logic while the first trade has not completed. Suggested object: Fields: If a new candidate has the same reason set while the position is still open: The duplicate block applies to the same reasons. It does not

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- ENT-R04 — Normalized Interpretation
  - Core Claim
  - Scenario-to-Position Transition
  - Duplicate Trade Block
  - Same Reasons vs New Reasons
  - PositionThread
  - Multi-Exit Logic
  - Hedge Separation
  - Opposite Scenario Handling
  - Split Orders and Logical Position
  - Position Completion
  - Machine-Readable Summary

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R02|ENT-R02.md]] — score `14`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R04|ENT-R04.md]] — score `12`
- [[docs/experience_capture/answers/ENT-R04/notes_en|notes_en.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `8`
- [[docs/architecture|architecture.md]] — score `8`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `8`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
