---
title: "D0009 H5 Atomic No-Sample Replay Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "2409"
entities:
  - "D0009"
  - "M0001"
concepts:
  - "Atomic No-Sample"
  - "Execution"
  - "Licensing"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# D0009 H5 Atomic No-Sample Replay Audit

**Source:** [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `2409` bytes

## خلاصه

D0009 is the strict H5 validator for the "do not build samples first" contract. It never calls `DAL_M0002CollectBranchSamples` and never creates `DALM0002BranchSample` arrays. The replay path is: Earlier H5 reports were useful structural/path research, but they could still inherit sample/order bias: branch samples were built first; samples were sorted by outcome/exit/entry order; multiple events known on the same candle could become a fake sequence; continuation R was normalized by a structural denominator even when no trading stop existed. D0009 removes that layer for validation. Regime state is derived directly from raw M0001 events that are already knowable by the current replay candle. F

## Headings

- D0009 H5 Atomic No-Sample Replay Audit
-   Why this exists
-   Regime construction
-   Entry model
-   Risk/R measurement
-   Key log lines

## Entities

`D0009`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/debug/H6_BOX_ALGORITHM_README|H6 Fast Box Visualizer — Official Algorithm]] — `debug_docs`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6 Fast Accurate Optionality Report]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
