
---
type: source_card
source_path: "docs/debug/E0007/README.md"
source_ext: ".md"
source_size: 4704
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook", "Rally", "UI / React", "Zone / RTV"]
entities: ["E0007"]
---

# Source Card — README.md

## Source

[[docs/debug/E0007/README|docs/debug/E0007/README.md]]

## Summary

E0007 is the first execution template for the idea that came from the purple-zone screenshots: > Purple is not the signal. Purple is the context. > The trade is the local source/revisit/extreme trigger that appears after the zone proves it is not dead. The screenshots were generated with `L=2`, so E0007 defaults to: The purple zones are an outcome map. A purple box means a zone eventually survived long enough. In live trading, we do not know that at the moment of first touch. So E0007 supports two different research modes: The EA does not require the future 500-bar survival label. It only asks whether the first touch: was confirmed, did not hunt the node, created enough first reaction, and can now be traded on the next revisit or secondary-node zone. This is not a live-valid execution mode. It is for reverse-engineering: "what if we only studied zones that later became purple-class zones

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0007

## Headings

- E0007 — Purple Source Extreme Executor Template
  - Why this is a template, not the final executor
    - 1. No-future/live-style source mode
    - 2. Oracle purple research mode
  - Entry modes
    - SOURCE_SECOND_REVISIT
    - SECONDARY_NODE_ZONE
    - EARLY_LADDER_STEP
  - Stop modes
  - Destination/R filter
  - Exit modes
  - Recommended initial tests

## Related Source Documents

- [[docs/debug/E0008/README|README.md]] — score `17`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `14`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-02/question_en|question_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-04/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
