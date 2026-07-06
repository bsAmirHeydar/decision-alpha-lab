---
title: "VAL0011 — Main Atomic No-Sample Unification"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/05_validation/VAL0011_main_atomic_no_sample_unification/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "1074"
entities:
  - "H0004"
  - "H0005"
  - "M0001"
  - "M0002"
  - "VAL0011"
concepts:
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# VAL0011 — Main Atomic No-Sample Unification

**Source:** [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|lab/05_validation/VAL0011_main_atomic_no_sample_unification/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `1074` bytes

## خلاصه

Promote the atomic no-sample contracts from debug validators into the main H0004 and H0005 Experts. A debug validator is useful, but the project should not keep correct logic only in debug files. If a debug contract is the right research contract, the main Expert must adopt it. The main H4 Expert should default to raw M0001 event known-time batches rather than completed M0002 branch sample sequences. The main H5 Expert should default to raw-event live-style replay rather than sample path reports. Continuation R should default to explicit risk, preferably ATR risk, rather than implicit structural path denominators. H4: H5: Classic sample/path reports may remain available as opt-in legacy diag

## Headings

- VAL0011 — Main Atomic No-Sample Unification
-   Purpose
-   Motivation
-   Main changes
-     H0004
-     H0005
-   Required sanity lines
-   Legacy mode

## Entities

`H0004`, `H0005`, `M0001`, `M0002`, `VAL0011`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[README|Decision Alpha Lab]] — `readme`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/03_validation/VAL0014_h4_atomic_full_stress_context/README|VAL0014 — H4 Atomic Full Stress + Human Context]] — `validation`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
