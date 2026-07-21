---
title: "H4 Deep Atomic Report + H6 Reversal Optionality"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "2519"
entities:
  - "M0002"
  - "M0004"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# H4 Deep Atomic Report + H6 Reversal Optionality

**Source:** [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `2519` bytes

## خلاصه

This release extends the official M0004 atomic/no-sample report without reintroducing M0002 samples or fake same-candle ordering. `sampleCalls=0` `branchSamplesBuilt=0` `m0002Calls=0` `sequenceOrder=known_time_batch_sequence` events known on the same candle/time are simultaneous mixed reversal/continuation batches are ambiguous and skipped from transition statistics Reports information-theoretic Markov memory over pure known-time batches: label entropy conditional entropy mutual information in bits predictability gain chi-square odds ratio Yule Q Reports the full run-length tail surface: p50, p75, p90, p95 run length for all/reversal/continuation share of reversal/continuation batches inside

## Headings

- H4 Deep Atomic Report + H6 Reversal Optionality
-   Contract
-   New H4 deep reports
-     `DAL_D0010_ATOMIC_INFORMATION`
-     `DAL_D0010_ATOMIC_RUN_DISTRIBUTION`
-     `DAL_D0010_ATOMIC_BATCH_INTENSITY`
-   New H6 report
-     Hypothesis
-     `DAL_H0006_OPTIONALITY_FAST/MAIN/SLOW`
-     `DAL_H0006_OPTIONALITY_STRESS_FAST/MAIN/SLOW`
-   Inputs

## Entities

`M0002`, `M0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
