
---
type: source_card
source_path: "docs/mql_native/M0002_HUNT_REJECT_EXIT_VOLATILITY.md"
source_ext: ".md"
source_size: 704
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Zone / RTV"]
entities: ["H0001", "H0002", "M0001", "M0002"]
---

# Source Card — M0002_HUNT_REJECT_EXIT_VOLATILITY.md

## Source

[[docs/mql_native/M0002_HUNT_REJECT_EXIT_VOLATILITY|docs/mql_native/M0002_HUNT_REJECT_EXIT_VOLATILITY.md]]

## Summary

This document is kept only as a historical note. The active M0002 module is not hunt/reject based. Use: Current logic: use exact M0001 completed-exit events with hunt/touch consumption preserved, classify the completed-exit candle close relative to `node_price`, and split the original M0001 event-window RTV into `REVERSAL_… H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, M0001, M0002

## Headings

- M0002 Hunt/Reject Document — Deprecated
  - Logic repair v1.70

## Related Source Documents

- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `35`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `27`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `27`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `27`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `27`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `27`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001_H0001_LOGIC_REPAIR_AUDIT.md]] — score `27`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `27`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `27`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
