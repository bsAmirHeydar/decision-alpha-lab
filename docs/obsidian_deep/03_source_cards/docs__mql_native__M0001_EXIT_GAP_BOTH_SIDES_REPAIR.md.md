
---
type: source_card
source_path: "docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR.md"
source_ext: ".md"
source_size: 1389
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Validation / Audit", "Zone / RTV"]
entities: ["H0002", "M0001"]
---

# Source Card — M0001_EXIT_GAP_BOTH_SIDES_REPAIR.md

## Source

[[docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR|docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR.md]]

## Summary

This repair locks the event lifecycle around the completed exit window. A touch event is completed only after `exit_gap` consecutive candles whose high/low do not intersect the frozen event territory. The exit can complete on either side of the frozen zone: rejection/reversal side, break/continuation side. The event must not be discarded simply because the node price was crossed during the pending touch window. The consume input still controls node lifecycle: `DAL_M0001_CONSUME_BY_TOUCH`: a confirmed touch consumes the node at the completed exit candle. `DAL_M0001_CONSUME_BY_HUNT`: a confirmed touch does not consume the node unless the node was hunted/broken during that completed touch event. If no hunt occurred, the node stays alive and the next territory cycle is reco… The RTV semantics remain unchanged: inside sample starts at event entry, the final `exit_gap` confirmation candles are

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0002, M0001

## Headings

- M0001 Exit-Gap Both-Sides Repair
  - Correct rule
  - Consumption timing
  - RTV
  - H0002 dependency

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `21`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `21`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `21`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `21`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `21`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `21`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `21`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `21`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `21`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
