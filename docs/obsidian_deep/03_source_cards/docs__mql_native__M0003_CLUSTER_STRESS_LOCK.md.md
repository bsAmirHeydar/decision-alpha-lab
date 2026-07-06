
---
type: source_card
source_path: "docs/mql_native/M0003_CLUSTER_STRESS_LOCK.md"
source_ext: ".md"
source_size: 1074
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "UI / React", "Validation / Audit"]
entities: ["H0001", "H0002", "H0003", "M0002", "M0003"]
---

# Source Card — M0003_CLUSTER_STRESS_LOCK.md

## Source

[[docs/mql_native/M0003_CLUSTER_STRESS_LOCK|docs/mql_native/M0003_CLUSTER_STRESS_LOCK.md]]

## Summary

This update hardens H0003 from a simple continuation-memory diagnostic into a full cluster-stress suite. Split M0003 inertia output into short non-truncated reports. Added per-horizon memory reports for each configured horizon. Added memory AUC and carry AUC summary. Added direct cluster comparison between reversal and continuation. Added deterministic Fisher-Yates lag-shuffle stress for lag-1 and lag-2 serial memory, with empirical p-values. Added direct branch-label permutation stress to test whether continuation-specific cluster memory survives label randomization. Added contiguous block cluster stress. Added configurable high-volatility run percentile. Added high-run iid expectation and run-over-iid ratio. Added high-run Fisher-Yates shuffle stress with empirical p-values. Added half-life status to shared H0001/H0002 horizon reports so `halfLifeH=0` is not misread as immediate decay.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0001, H0002, H0003, M0002, M0003

## Headings

- M0003 Cluster Stress Lock
  - Changes
  - Build targets

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `32`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `32`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `32`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `32`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `32`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `29`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `25`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `25`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `22`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
