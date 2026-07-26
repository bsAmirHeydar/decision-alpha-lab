
---
type: source_card
source_path: "lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README.md"
source_ext: ".md"
source_size: 764
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["D0010", "H0004", "M0001", "VAL0010"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README.md]]

## Summary

Purpose: validate H0004 regime clustering without branch samples and without fake same-candle sequences. A regime label becomes usable only at its `known_time`. All raw M0001 events that become known on that same candle are simultaneous. They cannot be interpreted as a sequence. Use D0010 output: `sampleCalls=0` `branchSamplesBuilt=0` `m0002Calls=0` `sameKnownTimeEventsAreSimultaneous=1` `ambiguousBatches` `sameTimeBatchCount` `DAL_D0010_ATOMIC_TRANSITION` `DAL_D0010_ATOMIC_PERM_STRESS` If same-time batches are frequent, old sample-sequence H4 reports were materially affected by fake sequencing. The D0010 transition matrix should be used instead.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

D0010, H0004, M0001, VAL0010

## Headings

- VAL0010 — H4 Atomic No-Sample Regime Replay
  - Validation rule
  - Pass/fail focus

## Related Source Documents

- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `28`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `25`
- [[lab/09_execution/mql5/README|README.md]] — score `23`
- [[docs/research_lessons_and_failure_modes|research_lessons_and_failure_modes.md]] — score `20`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `20`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `20`
- [[README|README.md]] — score `20`
- [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] — score `18`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|README.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
