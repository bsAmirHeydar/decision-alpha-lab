---
title: "EXE0005 — Continuation Close-Break Fixed-R"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_execution/EXE0005_continuation_close_break_fixed_r/README.md"
source_ext: ".md"
category: "execution"
source_size_bytes: "860"
entities:
  - "E0003"
  - "E0005"
  - "EXE0005"
  - "H0005"
  - "M0002"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# EXE0005 — Continuation Close-Break Fixed-R

**Source:** [[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|lab/04_execution/EXE0005_continuation_close_break_fixed_r/README.md]]

**Category:** `execution`  
**Status:** ok  
**Size:** `860` bytes

## خلاصه

This execution module tests the clean continuation idea separately from trailing/regime-exit models. It enters after a confirmed structural node is broken by candle close while the H0005/M0002 regime is continuation. E0005 is intentionally different from E0003. E0003 can be a trailing/regime-exit continuation executor. E0005 is a fixed-reward continuation executor, designed for clean statistical comparison of continuation close-break entries with fixed R exits.

## Headings

- EXE0005 — Continuation Close-Break Fixed-R
-   Purpose
-   Main idea
-   Main inputs
-   Notes

## Entities

`E0003`, `E0005`, `EXE0005`, `H0005`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/03_validation/VAL0006_h5_live_touch_replay/README|VAL0006 — H5 live-valid touch-entry replay]] — `validation`
- [[lab/03_validation/VAL0007_h5_causal_live_replay/README|VAL0007 — H5 Causal Live Replay]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
