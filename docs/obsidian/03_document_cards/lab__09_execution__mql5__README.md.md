---
title: "MQL5 Execution and Validation Layer"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/mql5/README.md"
source_ext: ".md"
category: "execution"
source_size_bytes: "1571"
entities:
  - "D0009"
  - "D0010"
  - "H0004"
  - "H0005"
  - "M0001"
concepts:
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "MQL Native"
  - "Validation"
---


# MQL5 Execution and Validation Layer

**Source:** [[lab/09_execution/mql5/README|lab/09_execution/mql5/README.md]]

**Category:** `execution`  
**Status:** ok  
**Size:** `1571` bytes

## خلاصه

MQL5 is the project layer used for fast replay, MetaTrader-native execution, and Expert Advisor validation. MQL5 is no longer only an execution bridge. It is also the strictest environment for live-style validation because it can replay candle state and execution policies close to the platform that will trade the system. Main hypothesis Experts must not depend on completed samples for live validity. For H0004 and H0005, the official direction is: Debug Experts are allowed to test new contracts. Once a contract is accepted, it must be moved into the main Expert or a shared include used by the main Expert. Accepted examples: D0010 proved H4 atomic no-sample regime batching. D0009 proved H5 ato

## Headings

- MQL5 Execution and Validation Layer
-   Current role
-   Official research rule
-   Debug vs main Experts
-   Execution reporting rule
-   Compile discipline

## Entities

`D0009`, `D0010`, `H0004`, `H0005`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[README|Decision Alpha Lab]] — `readme`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[docs/research_lessons_and_failure_modes|Research Lessons and Failure Modes]] — `core_docs`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
