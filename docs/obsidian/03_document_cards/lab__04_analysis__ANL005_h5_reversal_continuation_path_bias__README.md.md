---
title: "ANL005 — H5 Reversal/Continuation Path Bias Review"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_analysis/ANL005_h5_reversal_continuation_path_bias/README.md"
source_ext: ".md"
category: "analysis"
source_size_bytes: "1083"
entities:
  - "ANL005"
concepts:
  - "Atomic No-Sample"
  - "Execution"
  - "Validation"
---


# ANL005 — H5 Reversal/Continuation Path Bias Review

**Source:** [[lab/04_analysis/ANL005_h5_reversal_continuation_path_bias/README|lab/04_analysis/ANL005_h5_reversal_continuation_path_bias/README.md]]

**Category:** `analysis`  
**Status:** ok  
**Size:** `1083` bytes

## خلاصه

Which H5 results are tradable, and which are only structural path statistics? The classic H5 report mixed structural path normalization with execution-like R metrics. Reversal fixed-R tests were closer to execution logic. Continuation path PF was not a real trading PF because continuation did not use a real initial stop in the classic report. Reversal showed short reaction behavior but weak full structural path performance. Practical implication: use touch-entry, test R1/R2, account for same-bar ambiguity and spread. Continuation showed large path potential. However, old PF must be retested with explicit risk. Practical implication: use ATR or structural stop, test close-break and intrabar-b

## Headings

- ANL005 — H5 Reversal/Continuation Path Bias Review
-   Question
-   Key finding
-   Reversal interpretation
-   Continuation interpretation
-   Research decision

## Entities

`ANL005`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[lab/03_validation/VAL0009_h5_atomic_no_sample_replay/README|VAL0009 — H5 Atomic No-Sample Replay]] — `validation`
- [[lab/03_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/03_validation/VAL0017_h6_fast_accurate/README|VAL0017 — H6 Fast Accurate Optionality]] — `validation`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
