---
title: "VAL_M0001_MQL_NATIVE"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/05_validation/VAL_M0001_MQL_NATIVE/report.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "504"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# VAL_M0001_MQL_NATIVE

**Source:** [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|lab/05_validation/VAL_M0001_MQL_NATIVE/report.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `504` bytes

## خلاصه

Visual and journal validation for the native MQL5 implementation of M0001. [ ] L-rule high node confirms exactly at `i + L`. [ ] L-rule low node confirms exactly at `i + L`. [ ] Marker is drawn on pivot candle. [ ] Active-from line, when enabled, is drawn at `i + L`. [ ] Event scan does not start before active-from. [ ] RTV fields match the event window and before-window lengths. [ ] Strategy Tester visual state does not require Python.

## Headings

- VAL_M0001_MQL_NATIVE
-   Scope
-   Checklist

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL001/report|Report]] — `validation`
- [[lab/03_experiments/EXP0000_sample/report|Report]] — `experiment`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|Report]] — `experiment`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
