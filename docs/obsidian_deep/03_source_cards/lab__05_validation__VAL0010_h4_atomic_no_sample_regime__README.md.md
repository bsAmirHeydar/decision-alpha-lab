
---
type: source_card
source_path: "lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README.md"
source_ext: ".md"
source_size: 1055
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["D0010", "H0004", "M0001", "M0002", "VAL0010"]
---

# Source Card — README.md

## Source

[[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README.md]]

## Summary

Validate H0004 without using M0002 branch samples. If D0010 still shows positive same-lift, lag-1 correlation, and run persistence after this contract, H0004 becomes much stronger than the old classic report. If the effect disappears, the old regime memory was mostly an artifact of completed-sample sequencing.

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

D0010, H0004, M0001, M0002, VAL0010

## Headings

- VAL0010 — H4 Atomic No-Sample Regime Validation
  - Purpose
  - Contract
  - Main expected log lines
  - Required audit fields
  - Interpretation

## Related Source Documents

- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `28`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `28`
- [[lab/09_execution/mql5/README|README.md]] — score `25`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `25`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `25`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|README.md]] — score `25`
- [[README|README.md]] — score `25`
- [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] — score `23`
- [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4_ATOMIC_FULL_STRESS_CONTEXT.md]] — score `23`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|README.md]] — score `23`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
