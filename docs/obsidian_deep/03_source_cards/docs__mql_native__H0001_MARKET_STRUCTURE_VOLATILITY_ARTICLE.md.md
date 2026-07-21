
---
type: source_card
source_path: "docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE.md"
source_ext: ".md"
source_size: 2815
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "H0003"]
---

# Source Card — H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE.md

## Source

[[docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE|docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE.md]]

## Summary

H0001 tests whether completed structural-node territory events generate materially higher relative volatility than length-matched random windows. The production MQL-native definition is intentionally event-based and avoi… Detect confirmed structural highs and lows using the L-rule. A node becomes active only after the right-side confirmation window has closed. Build a node territory from the node price and the current structural extreme. The territory is frozen at first touch. Start the event when a candle intersects the frozen territory. Continue the event while candles keep touching or intersecting the territory. Complete the event after `exit_gap` consecutive candles are fully outside the frozen territory. A candle is fully outside if either its low is above the upper territory bound or its high is below the lower territory boun… Exclude the final exit-gap candles from the RTV inside

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0003

## Headings

- H0001 — Structural Node Territory Volatility
  - Abstract
  - Algorithm
  - Consumption lifecycle
  - Validation stack
  - Interpretation
  - Horizon half-life reporting guardrail

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `26`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `26`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `26`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `26`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `26`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `26`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `25`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `24`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `24`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
