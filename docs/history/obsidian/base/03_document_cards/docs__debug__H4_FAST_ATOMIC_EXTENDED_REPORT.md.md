---
title: "H4 Fast Atomic Extended Report"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "825"
concepts:
  - "Atomic No-Sample"
  - "Known-Time Causality"
  - "Validation"
---


# H4 Fast Atomic Extended Report

**Source:** [[docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT|docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `825` bytes

## خلاصه

This update keeps the official H4 report no-sample and fast, while restoring useful diagnostics that were previously only visible in the legacy sample report. The report still uses `sampleCalls=0`, `branchSamplesBuilt=0`, `m0002Calls=0`, and `m0001ComputePasses=1`. It does not run strict prefix replay by default. New lightweight outputs: `DAL_D0010_ATOMIC_LAG_DECAY` `DAL_D0010_ATOMIC_RUN_LENGTH_TRANSITION` `DAL_D0010_ATOMIC_BLOCK_PROFILE_FAST` `DAL_D0010_ATOMIC_BLOCK_PROFILE_MAIN` `DAL_D0010_ATOMIC_BLOCK_PROFILE_SLOW` These diagnostics are computed over pure known-time batches, so events that become known on the same candle are never treated as sequential. Mixed reversal/continuation batches

## Headings

- H4 Fast Atomic Extended Report

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL001/report|Report]] — `validation`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[lab/03_experiments/EXP0000_sample/report|Report]] — `experiment`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|Report]] — `experiment`
- [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008 / H0004 Causal Known-Candle Batch Report]] — `debug_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4 Atomic Full Stress + Human Context Diagnostics]] — `debug_docs`
- [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4 Deep Atomic Report + H6 Reversal Optionality]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
