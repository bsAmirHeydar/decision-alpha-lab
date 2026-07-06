
---
type: source_card
source_path: "docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING.md"
source_ext: ".md"
source_size: 17438
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "H0003", "H0004", "M0001", "M0002", "M0004"]
---

# Source Card — H0004_BRANCH_REGIME_CLUSTERING.md

## Source

[[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING.md]]

## Summary

H0004 asks whether reversal and continuation are only independent labels on completed node-territory events, or whether they form branch regimes with inertia. Core question: This is different from H0003. H0003 tests volatility-memory inside each branch. H0004 tests memory of the branch labels themselves. H0004 is a regime-state hypothesis. H0004 uses the same locked event stack: H0001 detects structural nodes and completed node-territory events. H0001 computes exact event RTV. H0002 labels each completed event as reversal or continuation. H0004 sorts valid M0002 branch samples chronologically by outcome/exit index. H0004 studies the branch-label sequence. No separate event builder is allowed. The null is not equal 50/50 labels. The null preserves the observed reversal/continuation counts and shuffles label order. This matters because reversal is usually more frequent than continuation. A

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0003, H0004, M0001, M0002, M0004

## Headings

- H0004 — Reversal/Continuation Branch Regime Clustering
  - Research question
  - Dependency chain
  - Null hypothesis
  - Primary metrics
    - Frequency model
    - Transition matrix
    - Lag correlation
    - Run clustering
    - Block concentration
  - Stress suite
  - Interpretation rules

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `48`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `48`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `48`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `43`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `38`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `38`
- [[README|README.md]] — score `37`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `36`
- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `35`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `34`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
