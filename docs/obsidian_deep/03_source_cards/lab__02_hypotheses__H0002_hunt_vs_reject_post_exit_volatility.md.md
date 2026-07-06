
---
type: source_card
source_path: "lab/02_hypotheses/H0002_hunt_vs_reject_post_exit_volatility.md"
source_ext: ".md"
source_size: 843
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Zone / RTV"]
entities: ["H0001", "H0002", "M0001", "M0002"]
---

# Source Card — H0002_hunt_vs_reject_post_exit_volatility.md

## Source

[[lab/02_hypotheses/H0002_hunt_vs_reject_post_exit_volatility|lab/02_hypotheses/H0002_hunt_vs_reject_post_exit_volatility.md]]

## Summary

This draft is kept only for history. It is not the active H0002 definition. The active hypothesis is: The active implementation is: Reason for deprecation: the second hypothesis is not a hunt/non-hunt split. It is a M0001 completed-exit branch split by the completed-exit candle close relative to the original node price, with the primary metric equal… H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, M0001, M0002

## Headings

- H0002 Hunt/Reject Draft — Deprecated
  - Logic repair v1.70

## Related Source Documents

- [[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility|H0002_reversal_vs_continuation_post_exit_volatility.md]] — score `30`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `28`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `28`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `28`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `28`
- [[README|README.md]] — score `28`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `26`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `26`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `26`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `26`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
