
---
type: source_card
source_path: "docs/experience_capture/answers/SCN-R04/answer_normalized_en.md"
source_ext: ".md"
source_size: 6719
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Hook", "Rally", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/SCN-R04/answer_normalized_en|docs/experience_capture/answers/SCN-R04/answer_normalized_en.md]]

## Summary

A scenario in NDS is born from a set of respected constraints. It remains alive, updates, reprices, loses rank, gains rank, or dies based on two main dimensions: The system does not need to decide scenario life/death by prediction correctness. It should track: A scenario is not a loose idea. It is an object created by a specific set of NDS constraints. Suggested object: Each ScenarioThread should keep: The source constraints are part of the scenario identity. The most important update signal is: Suggested metric: This score should reflect whether the original reasons for the scenario are still structurally valid. Examples of constraints that may need integrity tracking: The phrase "untouched constraints" should not mean only price not touching a level. It means: A constraint can be untouched, partially weakened, consumed, invalidated, or replaced. Suggested states: A scenario is also eva

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- SCN-R04 — Normalized Interpretation
  - Core Claim
  - Scenario as Constraint-Based Object
  - Constraint Integrity
  - Untouched Constraint Rule
  - Relative Weight
  - Scenario Update
  - Scenario Repricing
  - Scenario Death
  - Veto vs Death
  - Watchlist
  - Rank and Weight Update

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/SCN-R03|SCN-R03.md]] — score `18`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-02/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
