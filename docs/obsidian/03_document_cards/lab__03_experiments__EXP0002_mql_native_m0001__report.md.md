---
title: "EXP0002 — MQL-native M0001 Runtime"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0002_mql_native_m0001/report.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "688"
entities:
  - "EXP0002"
  - "M0001"
concepts:
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# EXP0002 — MQL-native M0001 Runtime

**Source:** [[lab/03_experiments/EXP0002_mql_native_m0001/report|lab/03_experiments/EXP0002_mql_native_m0001/report.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `688` bytes

## خلاصه

Move M0001 from a Python/MQL bridge into a pure MQL5 runtime while preserving the lab research workflow. A native MQL5 implementation will produce faster, clearer, and more live-safe visual validation than an external Python bridge because the detector, event engine, tester timeline, and chart objects live in the same runtime. L-rule nodes appear only after `L` right-side candles exist. Markers point to the true pivot candle. Event construction starts only from `active_from_index`. No future candles are available to the engine. Visual redraw is synchronous with MT5 tester time.

## Headings

- EXP0002 — MQL-native M0001 Runtime
-   Objective
-   Hypothesis
-   Validation Target

## Entities

`EXP0002`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL001/report|Report]] — `validation`
- [[lab/03_experiments/EXP0000_sample/report|Report]] — `experiment`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|Report]] — `experiment`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/articles/structural_regime_memory_without_samples|Article — Structural Regime Memory Without Samples]] — `article_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
