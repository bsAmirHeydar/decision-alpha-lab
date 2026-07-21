
---
type: source_card
source_path: "docs/articles/structural_regime_memory_without_samples.md"
source_ext: ".md"
source_size: 2823
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["H0004", "M0001", "M0002"]
---

# Source Card — structural_regime_memory_without_samples.md

## Source

[[docs/articles/structural_regime_memory_without_samples|docs/articles/structural_regime_memory_without_samples.md]]

## Summary

A central question of Decision Alpha Lab is whether structural market regimes have memory. Early reports suggested that reversal and continuation labels cluster: a reversal label is more likely to be followed by another… A key flaw was then identified: several labels may become knowable on the same candle. If those labels are sorted into a sequence, the report can create transitions that never existed in live time. This article documents the move from sample sequencing to atomic known-time regime batching. Branch samples are convenient. They compress a market event into one object with entry, exit, outcome, and label fields. The problem is that the sample is only complete after the event has already resolved. Sorting completed samples by outcome or entry may be useful for retrospective analysis, but it is not automatically a live-valid regim… A sample sequence can answer: > In what order

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0004, M0001, M0002

## Headings

- Article — Structural Regime Memory Without Samples
  - Abstract
  - The problem with sample order
  - The same-candle sequencing flaw
  - Atomic known-time batches
  - Why this matters
  - The current standard

## Related Source Documents

- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `25`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `25`
- [[README|README.md]] — score `25`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `23`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `23`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `23`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `23`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `23`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004_branch_regime_clustering.md]] — score `23`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `23`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
