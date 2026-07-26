
---
type: source_card
source_path: "docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md"
source_ext: ".md"
source_size: 1911
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Execution / Risk", "Known-Time Causality", "MQL Native", "UI / React", "Validation / Audit"]
entities: ["M0001", "M0002", "M0004", "M0005"]
---

# Source Card — MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md

## Source

[[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]]

## Summary

This release moves the no-sample / live-style contract into the main M0004 and M0005 experts. The main reports now default to atomic raw M0001 event replay: no `DALM0002BranchSample` sequence is built by the official main report path no M0002 branch-sample collector is called by the official main report path regime order is based on the candle/time at which raw M0001 events become knowable raw events known on the same candle are treated as simultaneous mixed reversal/continuation batches are marked ambiguous and skipped from transition/path statistics by default `M0004_BranchRegimeClustering.mq5` now calls `DAL_M0004RunAtomicNoSampleReport()` by default. Official audit line: The legacy sample-based report remains available only if explicitly enabled: Default is false. `M0005_DirectionalMemory.mq5` now calls `DAL_M0005RunAtomicNoSampleReplay()` by default. Official audit lines: Continuati

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001, M0002, M0004, M0005

## Headings

- Main Atomic No-Sample Unification for H4/H5
  - Contract
  - M0004
  - M0005
  - Why

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `32`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `26`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|README.md]] — score `25`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `24`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `24`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `23`
- [[README|README.md]] — score `22`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `21`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `21`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
