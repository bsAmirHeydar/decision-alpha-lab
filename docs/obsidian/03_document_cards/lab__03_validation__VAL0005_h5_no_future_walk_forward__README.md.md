---
title: "VAL0005 — H5 No-Future Walk-Forward Validation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0005_h5_no_future_walk_forward/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "1306"
entities:
  - "H0005"
  - "M0001"
  - "M0002"
  - "VAL0005"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# VAL0005 — H5 No-Future Walk-Forward Validation

**Source:** [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|lab/03_validation/VAL0005_h5_no_future_walk_forward/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `1306` bytes

## خلاصه

Validation target: H0005 must be evaluated exactly as it would be available live. H5 must not be validated by building a complete historical array once and then asking earlier candles what the future-completed node/regime was. The validation process must advance one candle at a time. Use: The debugger replays history using prefix-only bar arrays. At each cursor candle it reconstructs: 1. M0001 structural nodes 2. M0001 events 3. M0002 latest branch regime The result is the regime that would have existed live at that candle. Primary pass condition: Secondary sanity conditions: Structural nodes need right-side confirmation. If a historical report treats a pivot node as known at the pivot candl

## Headings

- VAL0005 — H5 No-Future Walk-Forward Validation
-   Rule
-   Implementation
-   Pass condition
-   Why this matters

## Entities

`H0005`, `M0001`, `M0002`, `VAL0005`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[README|Decision Alpha Lab]] — `readme`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|EXE0005 — Continuation Close-Break Fixed-R]] — `execution`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[lab/03_validation/VAL0013_h4_fast_atomic_extended/README|VAL0013 — H4 Fast Atomic Extended Diagnostics]] — `validation`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/03_validation/VAL0006_h5_live_touch_replay/README|VAL0006 — H5 live-valid touch-entry replay]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
