
---
type: source_card
source_path: "lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility_deep_audit.md"
source_ext: ".md"
source_size: 987
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "M0001"]
---

# Source Card — H0002_reversal_vs_continuation_post_exit_volatility_deep_audit.md

## Source

[[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility_deep_audit|lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility_deep_audit.md]]

## Summary

H0002 splits completed M0001 exit events into reversal and continuation branches by close versus the original node price at the completed exit candle. It must not filter by hunt/touch outcome before classification. It must not measure a separate post-outcome fixed window by default. The branch label splits the same M0001 event RTV. Primary evidence lines: Full stability lines for each branch: H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, M0001

## Headings

- H0002 Deep Audit
  - Logic repair v1.70

## Related Source Documents

- [[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility|H0002_reversal_vs_continuation_post_exit_volatility.md]] — score `28`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `27`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `27`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `27`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `27`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `27`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `27`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `27`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
