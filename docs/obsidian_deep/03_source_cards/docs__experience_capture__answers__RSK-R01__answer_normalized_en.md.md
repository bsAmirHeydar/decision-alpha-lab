
---
type: source_card
source_path: "docs/experience_capture/answers/RSK-R01/answer_normalized_en.md"
source_ext: ".md"
source_size: 5671
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/RSK-R01/answer_normalized_en|docs/experience_capture/answers/RSK-R01/answer_normalized_en.md]]

## Summary

Risk budget in NDS must be learned and measured across three structural levels: Risk is not one flat value. The system should measure how expensive or clean each layer is, and how much aggregate risk is being tolerated for a given profit potential and reward. Recommended canonical model: The user explicitly defines three levels: Each level can make the trade more or less expensive. The final risk score should be an aggregate result of these layers. Suggested hierarchy: Context defines the background cost of the decision. Zone defines the cost of exploiting the context. Entry defines the precise execution cost and stop geometry. At the context level, the system should learn: A context can be expensive if it produces: A context can be cleaner if it produces: At the zone level, the system should learn which zones are: Zone risk may depend on: A zone with good context may still be too expens

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- RSK-R01 — Normalized Interpretation
  - Core Claim
  - Three Risk Levels
  - Context-Level Risk
  - Zone-Level Risk
  - Entry-Level Risk
  - Aggregate Risk Tolerance
  - Risk in Exchange for Reward
  - Scoring
  - Training Requirement
  - Risk Budget Allocation
  - Veto Logic

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `12`
- [[docs/debug/E0006/README|README.md]] — score `12`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `12`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `12`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `12`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/ENT-R01/answer_normalized_en|answer_normalized_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
