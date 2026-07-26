
---
type: source_card
source_path: "lab/03_validation/VAL0012_h4_fast_atomic_main/README.md"
source_ext: ".md"
source_size: 987
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Known-Time Causality", "MQL Native", "UI / React", "Validation / Audit"]
entities: ["H0004", "M0001", "M0002", "M0004", "VAL0012"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0012_h4_fast_atomic_main/README|lab/03_validation/VAL0012_h4_fast_atomic_main/README.md]]

## Summary

This validation release makes the official H0004 main report fast enough for routine MetaTrader runs while preserving the no-sample known-time-batch contract. No M0002 branch samples. Raw M0001 events only. Events known on the same candle/time are simultaneous. Mixed reversal/continuation batches are ambiguous and skipped from transition statistics. Main report uses one M0001 pass by default. Strict prefix replay remains opt-in for small audits. `InpAtomicReportMode` is now an int input for MetaEditor safety: `0` fast official report, `1` strict prefix replay for small debug runs. Installer syncs the M0004 include to all local terminal include trees.

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0004, M0001, M0002, M0004, VAL0012

## Headings

- VAL0012 — H4 Fast Atomic Main Report
  - Contract
  - Expected audit markers
    - Release 1.01 compile fix

## Related Source Documents

- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `28`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `26`
- [[README|README.md]] — score `25`
- [[docs/architecture|architecture.md]] — score `25`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `25`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] — score `25`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `24`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `24`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `24`
- [[lab/02_hypotheses/H0004_branch_regime_clustering|H0004_branch_regime_clustering.md]] — score `24`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
