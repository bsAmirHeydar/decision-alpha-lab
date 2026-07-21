---
title: "VAL0013 — H4 Fast Atomic Extended Diagnostics"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0013_h4_fast_atomic_extended/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "582"
entities:
  - "M0001"
  - "M0002"
  - "VAL0013"
concepts:
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# VAL0013 — H4 Fast Atomic Extended Diagnostics

**Source:** [[lab/03_validation/VAL0013_h4_fast_atomic_extended/README|lab/03_validation/VAL0013_h4_fast_atomic_extended/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `582` bytes

## خلاصه

Purpose: restore rich H4 reporting without returning to the old sample-based report or the heavy strict prefix replay. Contract: No M0002 branch samples. No outcome-sorted sample sequence. Raw M0001 events are grouped by known candle/time. Same-known-time events are simultaneous. Mixed reversal/continuation batches are ambiguous and skipped. M0001 is computed once in the main fast mode. Use `InpAtomicPrintExtendedReport=true` to print lightweight lag decay, run-length transition, and block profile diagnostics.

## Headings

- VAL0013 — H4 Fast Atomic Extended Diagnostics

## Entities

`M0001`, `M0002`, `VAL0013`

## Concepts

- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
