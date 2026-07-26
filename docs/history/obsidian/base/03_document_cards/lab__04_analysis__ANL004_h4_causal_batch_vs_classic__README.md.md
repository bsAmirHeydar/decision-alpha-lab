---
title: "ANL004 — H4 Classic vs Causal Batch Analysis"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_analysis/ANL004_h4_causal_batch_vs_classic/README.md"
source_ext: ".md"
category: "analysis"
source_size_bytes: "790"
entities:
  - "ANL004"
  - "H0004"
concepts:
  - "Atomic No-Sample"
  - "Known-Time Causality"
  - "NDS Anatomy"
---


# ANL004 — H4 Classic vs Causal Batch Analysis

**Source:** [[lab/04_analysis/ANL004_h4_causal_batch_vs_classic/README|lab/04_analysis/ANL004_h4_causal_batch_vs_classic/README.md]]

**Category:** `analysis`  
**Status:** ok  
**Size:** `790` bytes

## خلاصه

How much did same-candle fake sequencing inflate H0004 regime memory? Causal batching reduced the reported memory but did not eliminate it. Classic sequence: samePct: 72.82%, sameLift: 19.80 percentage points, lag1Corr: 0.4214. Causal known-candle pure batches: samePct: 65.61%, sameLift: 11.98 percentage points, lag1Corr: 0.2584. The old report was too optimistic, but not entirely fake. Roughly speaking, part of the effect was sequencing artifact, and part remained after removing same-time ambiguity. Classic H4 should remain as a historical/debug reference only. Official H4 claims should use atomic no-sample known-time batches.

## Headings

- ANL004 — H4 Classic vs Causal Batch Analysis
-   Question
-   Key finding
-   Interpretation
-   Research decision

## Entities

`ANL004`, `H0004`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[lab/03_validation/VAL0014_h4_atomic_full_stress_context/README|VAL0014 — H4 Atomic Full Stress + Human Context]] — `validation`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[lab/03_validation/VAL0016_h6_standalone_optionality/README|VAL0016 — H6 standalone optionality edge map]] — `validation`
- [[lab/03_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/03_validation/VAL0017_h6_fast_accurate/README|VAL0017 — H6 Fast Accurate Optionality]] — `validation`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
