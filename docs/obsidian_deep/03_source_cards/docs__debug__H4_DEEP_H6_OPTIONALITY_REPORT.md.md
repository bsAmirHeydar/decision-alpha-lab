
---
type: source_card
source_path: "docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT.md"
source_ext: ".md"
source_size: 2519
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Convexity / Optionality", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["M0002", "M0004"]
---

# Source Card — H4_DEEP_H6_OPTIONALITY_REPORT.md

## Source

[[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT.md]]

## Summary

This release extends the official M0004 atomic/no-sample report without reintroducing M0002 samples or fake same-candle ordering. `sampleCalls=0` `branchSamplesBuilt=0` `m0002Calls=0` `sequenceOrder=known_time_batch_sequence` events known on the same candle/time are simultaneous mixed reversal/continuation batches are ambiguous and skipped from transition statistics Reports information-theoretic Markov memory over pure known-time batches: label entropy conditional entropy mutual information in bits predictability gain chi-square odds ratio Yule Q Reports the full run-length tail surface: p50, p75, p90, p95 run length for all/reversal/continuation share of reversal/continuation batches inside 5+ and 10+ length runs Reports same-time batch intensity and direction structure: mean event count per batch by regime multi-event batch percentage 3+ event batch percentage p90 event count buy/sell/

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0002, M0004

## Headings

- H4 Deep Atomic Report + H6 Reversal Optionality
  - Contract
  - New H4 deep reports
    - `DAL_D0010_ATOMIC_INFORMATION`
    - `DAL_D0010_ATOMIC_RUN_DISTRIBUTION`
    - `DAL_D0010_ATOMIC_BATCH_INTENSITY`
  - New H6 report
    - Hypothesis
    - `DAL_H0006_OPTIONALITY_FAST/MAIN/SLOW`
    - `DAL_H0006_OPTIONALITY_STRESS_FAST/MAIN/SLOW`
  - Inputs

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `22`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `21`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] — score `21`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `21`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `20`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `19`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `19`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `18`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `18`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
