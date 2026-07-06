
---
type: source_card
source_path: "docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md"
source_ext: ".md"
source_size: 2346
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "H0003", "M0001", "M0002"]
---

# Source Card — H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md

## Source

[[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]]

## Summary

H0002 classifies exact H0001/M0001 completed node-territory events into two node-side branches at the completed exit candle: reversal and continuation. The measurement remains locked to the original M0001 event RTV windo… For a LOW node, a completed exit close above the node price is `REVERSAL_AFTER_EXIT`, and a completed exit close below the node price is `CONTINUATION_AFTER_EXIT`. For a HIGH node, the mapping is inverted: a close below… The emerging model is not merely “which branch is higher.” It has four dimensions: Frequency: reversal is the higher-frequency branch, while continuation tends to occur less often. Intensity: continuation tends to produce higher event RTV and higher logRTV than reversal. Tail: continuation tends to show fatter right-tail behavior, especially in P90/P95 and CVaR90/CVaR95. Memory: continuation tends to preserve higher post-event horizon volatility than re

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0003, M0001, M0002

## Headings

- H0002 — Reversal vs Continuation Branch Volatility Model
  - Abstract
  - Branch definition
  - Branch model
  - Reporting
  - Interpretation
  - Relation to H0003

## Related Source Documents

- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `38`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `38`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `36`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `36`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `36`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `36`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `36`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `33`
- [[README|README.md]] — score `32`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `31`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
