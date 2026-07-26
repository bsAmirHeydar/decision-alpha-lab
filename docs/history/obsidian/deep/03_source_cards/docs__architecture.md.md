
---
type: source_card
source_path: "docs/architecture.md"
source_ext: ".md"
source_size: 3634
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Atomic No-Sample", "Decision Node", "Execution / Risk", "Known-Time Causality", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001", "M0002", "M0004", "M0005"]
---

# Source Card — architecture.md

## Source

[[docs/architecture|docs/architecture.md]]

## Summary

Decision Alpha Lab uses a layered architecture for structural market research and execution. The project does not assume that fixed time windows are the natural unit of market analysis. The core unit is a structural event: node, zone, revisit, hunt, break, known-time regime, and execution opportunity. Python remains useful for: data engineering, large-scale offline analysis, feature extraction, visualization, exploratory statistics, parameter sweeps, external data pipelines. Python is allowed to discover ideas. It must not be the only source of live-valid execution claims unless its replay is strictly causal. MQL5 is responsible for: MetaTrader-native replay, Expert Advisor execution, broker-facing order management, live-style state reconstruction, stop/target/trailing modeling, execution logs, validation close to the final trading environment. MQL5 can now contain research validators wh

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001, M0002, M0004, M0005

## Headings

- System Architecture
  - Research philosophy
  - Python layer
  - MQL5 layer
  - Core modules
    - M0001 — Structural node and event lifecycle
    - M0002 — Branch sample pairing
    - M0004 — Regime memory
    - M0005 — Directional memory
  - Validation hierarchy
  - Design principle
  - Astro stack

## Related Source Documents

- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] — score `32`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `31`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `29`
- [[README|README.md]] — score `28`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `27`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `27`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `27`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `27`
- [[lab/02_hypotheses/H0004_branch_regime_clustering|H0004_branch_regime_clustering.md]] — score `27`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `26`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
