
---
type: source_card
source_path: "docs/mql_native/MODULE_MAP.md"
source_ext: ".md"
source_size: 4688
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "H0003", "H0004", "M0001", "M0002", "M0003", "M0004"]
---

# Source Card — MODULE_MAP.md

## Source

[[docs/mql_native/MODULE_MAP|docs/mql_native/MODULE_MAP.md]]

## Summary

Version: 1.66 Removed legacy layers are intentionally not part of the active runtime: The M0001 MQL-native engine now includes a final-only professional validation layer: compact NODES/RANDOM reports, explicit effect-size metrics, paired validation, bootstrap confidence intervals, sign-flip permutation p-… See `docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS.md`. M0002 is isolated from M0001 at the EA and include-folder level. It reuses M0001 structural-node, territory, log-range, and reporting modules, but uses the exact M0001 event lifecycle so H0002 is not inflated by post-con… See `docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md`. H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed. M0004 studies the chronological sequence of exa

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0003, H0004, M0001, M0002, M0003, M0004

## Headings

- MQL Module Map
  - v1.60 Professional Validation Metrics
  - v1.66 M0002 Neutral Reversal/Continuation EVENT_RTV Branch Lab
  - Logic repair v1.70
  - v1.00 M0004 Branch-Regime Clustering

## Related Source Documents

- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `56`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `53`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `53`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `48`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `45`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `45`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `43`
- [[lab/02_hypotheses/H0004_branch_regime_clustering|H0004_branch_regime_clustering.md]] — score `40`
- [[README|README.md]] — score `39`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `38`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
