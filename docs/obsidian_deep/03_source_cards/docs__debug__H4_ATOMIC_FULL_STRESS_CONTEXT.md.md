
---
type: source_card
source_path: "docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT.md"
source_ext: ".md"
source_size: 1660
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Execution / Risk", "Known-Time Causality", "Validation / Audit"]
entities: ["H0004", "M0001", "M0002"]
---

# Source Card — H4_ATOMIC_FULL_STRESS_CONTEXT.md

## Source

[[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT.md]]

## Summary

This release restores the full stress/test surface for the official H0004 atomic no-sample report while preserving the strict contract: no M0002 branch samples no sample order no same-candle fake sequencing raw M0001 events only known-time batches only mixed reversal/continuation batches skipped from transitions by default Stress groups can now be enabled or disabled independently: `InpAtomicStressTransitionPermutation` `InpAtomicStressRunShuffle` `InpAtomicStressBlockConcentration` `InpAtomicStressCircularShift` `InpAtomicStressLocalBlockShuffle` `InpAtomicStressContextShuffle` Human-context diagnostics are controlled by: `InpAtomicPrintHumanContextReport` `InpAtomicContextLookbackFast` `InpAtomicContextLookbackMain` `InpAtomicContextLookbackSlow` `InpAtomicContextEwmaAlpha` `InpAtomicContextStrongThreshold` The official atomic report can now print: `DAL_D0010_ATOMIC_RUN_SHUFFLE_STRESS`

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0004, M0001, M0002

## Headings

- H4 Atomic Full Stress + Human Context Diagnostics
  - Added input toggles
  - Added report lines
  - Interpretation

## Related Source Documents

- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `23`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `23`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `23`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|README.md]] — score `23`
- [[README|README.md]] — score `23`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `22`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `22`
- [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] — score `21`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|README.md]] — score `21`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
