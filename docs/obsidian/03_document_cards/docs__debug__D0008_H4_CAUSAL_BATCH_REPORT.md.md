---
title: "D0008 / H0004 Causal Known-Candle Batch Report"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/D0008_H4_CAUSAL_BATCH_REPORT.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "1630"
entities:
  - "D0008"
  - "H0004"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# D0008 / H0004 Causal Known-Candle Batch Report

**Source:** [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|docs/debug/D0008_H4_CAUSAL_BATCH_REPORT.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `1630` bytes

## خلاصه

This release fixes the main H0004 live-validity ambiguity: multiple branch samples can become knowable on the same candle. The classic H0004 report sorts samples by `outcome_index`, then by `entry_index`, then by `id`. That is acceptable as an exploratory sample sequence, but it can create fake within-candle transitions when several highs/lows are confirmed on the same bar. The new causal batch layer groups samples by their knowable candle: `known_index = outcome_index` when available else `exit_index` else `entry_index` All samples with the same `known_index` are treated as simultaneous. A batch with only reversal labels is a reversal batch. A batch with only continuation labels is a contin

## Headings

- D0008 / H0004 Causal Known-Candle Batch Report

## Entities

`D0008`, `H0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007 — H5 Causal Live Replay Audit]] — `debug_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[docs/research_lessons_and_failure_modes|Research Lessons and Failure Modes]] — `core_docs`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/05_validation/VAL001/report|Report]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
