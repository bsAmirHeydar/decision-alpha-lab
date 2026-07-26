
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_GLOSSARY.md"
source_ext: ".md"
source_size: 4844
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — CONCEPT_GLOSSARY.md

## Source

[[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_GLOSSARY|docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_GLOSSARY.md]]

## Summary

The only raw price observations used by the structural logic. Open, close, body, candle direction, and candle color are not structural inputs. A high or low price point that satisfies the project node definition for a given L. A node is extracted from candle highs/lows and remains historically valid after it is created. The project node clearance parameter: A high node requires at least L candles on the left and L candles on the right that do not reach that high price. A low node requires at least L candles on the left and L candles on the right that do not reach that low price. Equal highs/lows are handled as plateau nodes by the existing project node module. A stable reference to a specific node. Identity is not only price. It must include time, price, side, L, plateau handling, and any project-level node id if available. Equality is not a break. A price must pass a boundary. Equal hig

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Concept Glossary
  - Candle High / Candle Low
  - Node
  - L
  - Node Identity
  - Equality
  - Pass / Break / Hit
  - Flag Body
  - Origin
  - Leg1
  - Waist
  - Leg2

## Related Source Documents

- [[docs/glossary|glossary.md]] — score `16`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
