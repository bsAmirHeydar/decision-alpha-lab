
---
type: source_card
source_path: "docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md"
source_ext: ".md"
source_size: 8406
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Licensing", "MQL Native", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "H0003", "M0001", "M0002", "M0003"]
---

# Source Card — H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md

## Source

[[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]]

## Summary

H0003 asks whether the higher volatility created inside a completed node-territory event behaves differently after the exit branch is known. The specific hypothesis is: > Continuation exits are lower-frequency than reversal exits, but the volatility produced around the zone has higher inertia, stronger post-event memory, fatter right-tail behavior, and more clustered high-volatility per… This is not a directional trading rule. It is a volatility-state hypothesis layered above H0001 and H0002. H0003 must not define a new event universe. It reuses the existing stack: **H0001 / M0001** builds the completed node-territory events, including node activation, dynamic territory, touch confirmation, frozen zone, two-sided exit-gap completion, and input-driven node consumption. **H0002 / M0002** labels each completed event as `REVERSAL_AFTER_EXIT` or `CONTINUATION_AFTER_EXIT` using the exit candle

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0003, M0001, M0002, M0003

## Headings

- H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence
  - Research question
  - Reuse policy and semantic lock
  - Core model
  - Primary metrics
    - 1. Event inertia
    - 2. Tail inertia
    - 3. Horizon memory
    - 4. Memory summary
    - 5. Cluster memory
    - 6. Cluster comparison
  - Cluster stress tests

## Related Source Documents

- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `45`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `43`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `43`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `43`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `38`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `38`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `38`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `36`
- [[README|README.md]] — score `36`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `35`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
