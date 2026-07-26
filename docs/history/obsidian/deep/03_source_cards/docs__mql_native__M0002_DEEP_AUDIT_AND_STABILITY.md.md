
---
type: source_card
source_path: "docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY.md"
source_ext: ".md"
source_size: 3174
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "M0001", "M0002"]
---

# Source Card — M0002_DEEP_AUDIT_AND_STABILITY.md

## Source

[[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY.md]]

## Summary

This patch hardens the second hypothesis after the H0001/H0002 logic repair. H0002 does **not** ask whether an event hunted or touched. It asks only: > At the candle where the exit-gap window is completed, where did the close finish relative to the original node price? For LOW nodes: `close > node_price` => `REVERSAL_AFTER_EXIT` `close < node_price` => `CONTINUATION_AFTER_EXIT` For HIGH nodes: `close < node_price` => `REVERSAL_AFTER_EXIT` `close > node_price` => `CONTINUATION_AFTER_EXIT` The measured value is locked to the native M0001 event RTV: The branch is only a label. It does not move the volatility window. `nodes` is the count of confirmed structural pivot nodes. `m0001Events` is the count of completed touch -> exit-gap cycles produced from those nodes. A single node can generate many M0001 cycles because M0002 previously used a neutral builder. That path is now deprecated; v1.70…

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, M0001, M0002

## Headings

- M0002 Deep Audit and Stability Suite
  - Purpose
  - Why m0001Events can be much larger than nodes
  - Random null engine
  - H2 stability suite
  - Logic repair v1.70

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `34`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `33`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `33`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `33`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `33`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `33`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `33`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `33`
- [[README|README.md]] — score `32`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `31`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
