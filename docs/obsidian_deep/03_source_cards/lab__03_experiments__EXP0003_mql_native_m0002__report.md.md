
---
type: source_card
source_path: "lab/03_experiments/EXP0003_mql_native_m0002/report.md"
source_ext: ".md"
source_size: 956
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Validation / Audit"]
entities: ["EXP0003", "H0001", "H0002", "M0001", "M0002"]
---

# Source Card — report.md

## Source

[[lab/03_experiments/EXP0003_mql_native_m0002/report|lab/03_experiments/EXP0003_mql_native_m0002/report.md]]

## Summary

This experiment runs the M0002 central Expert Advisor. It reuses M0001 structural-node detection, territory math, log-range utilities, and reporting metrics, but uses M0001 completed-exit events with M0001 hunt/touch con… Expected output prefixes: H0002 now uses `DAL_M0001ComputeEvents()` directly. Node lifetime is preserved exactly as in H0001/M0001. The selected `InpConsumeMode` decides whether a confirmed touch consumes the node or whether the node remains aliv…

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0003, H0001, H0002, M0001, M0002

## Headings

- EXP0003 — M0002 Reversal/Continuation Exit Volatility
  - Logic repair v1.70

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `28`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `28`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `28`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `28`
- [[README|README.md]] — score `28`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `26`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `26`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `26`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `26`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001_H0001_LOGIC_REPAIR_AUDIT.md]] — score `26`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
