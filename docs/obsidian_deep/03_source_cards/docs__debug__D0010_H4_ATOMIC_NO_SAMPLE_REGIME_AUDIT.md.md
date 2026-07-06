
---
type: source_card
source_path: "docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md"
source_ext: ".md"
source_size: 1554
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Decision Node", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["D0010", "H0004", "M0001", "M0002", "M0004"]
---

# Source Card — D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md

## Source

[[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]]

## Summary

D0010 is the strict live-style validator for H0004 regime memory. It removes M0002 branch samples from the H4 validation path: no `DALM0002BranchSample` no `DAL_M0002CollectBranchSamples` no outcome-sorted sample sequence no artificial sequencing of regimes that become knowable on the same candle At each replay step, D0010 uses only closed bars available up to that candle: Build confirmed structural nodes from the prefix. Build raw M0001 events from the prefix. Classify only raw events whose `known_index` equals the current decision candle. Treat all events with the same `known_time` as one simultaneous batch. If a batch contains both reversal and continuation labels, mark it ambiguous and skip it from transition/run statistics by default. Compute transition and run memory only between pure batches with different known times. `DAL_D0010_AUDIT` `DAL_D0010_ATOMIC_TRANSITION` `DAL_D0010_ATO

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

D0010, H0004, M0001, M0002, M0004

## Headings

- D0010 — H4 Atomic No-Sample Regime Audit
  - Contract
  - Important output lines
  - Interpretation

## Related Source Documents

- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `28`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `28`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `28`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `28`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `28`
- [[lab/02_hypotheses/H0004_branch_regime_clustering|H0004_branch_regime_clustering.md]] — score `28`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|README.md]] — score `28`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `27`
- [[README|README.md]] — score `27`
- [[docs/architecture|architecture.md]] — score `27`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
