---
title: "EXP0005 — MQL-native H0005 directional memory"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0005_mql_native_directional_memory/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1313"
entities:
  - "EXP0005"
  - "H0005"
  - "M0005"
concepts:
  - "Execution"
  - "MQL Native"
  - "Validation"
---


# EXP0005 — MQL-native H0005 directional memory

**Source:** [[lab/03_experiments/EXP0005_mql_native_directional_memory/README|lab/03_experiments/EXP0005_mql_native_directional_memory/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1313` bytes

## خلاصه

Run `M0005_DirectionalMemory.mq5` in MetaTrader Strategy Tester. Expected build sanity line: Key checks: 1. `DAL_M0005_FINAL_OUTCOME_REVERSAL` — structural target success for reversal paths. 2. `DAL_M0005_FINAL_OUTCOME_CONTINUATION` — continuation follow-through before regime change. 3. `DAL_M0005_FINAL_EXCURSION_*` — MFE/MAE until path exit. 4. `DAL_M0005_FINAL_REALIZED_R_*` — realized win rate, R:R, profit factor, and expectancy R. 5. `DAL_M0005_FINAL_FLOATING_R_*` — floating MFE/MAE R, floating R:R, and R-based first-hit order. 6. `DAL_M0005_FINAL_RANDOM_PERFORMANCE_*` — actual versus matched-random win rate, profit factor, expectancy R, MFE R, and floating R:R. 7. `DAL_M0005_FINAL_STRESS

## Headings

- EXP0005 — MQL-native H0005 directional memory

## Entities

`EXP0005`, `H0005`, `M0005`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_validation/VAL0006_h5_live_touch_replay/README|VAL0006 — H5 live-valid touch-entry replay]] — `validation`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/03_experiments/EXP0005_mql_native_m0004_contextual_branch_state/README|EXP0005 — MQL-native contextual branch-state diagnostics]] — `experiment`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/03_validation/VAL0007_h5_causal_live_replay/README|VAL0007 — H5 Causal Live Replay]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[docs/mql_native/H0005_DIRECTIONAL_MEMORY|H0005 — Directional Memory of Structural Regimes]] — `mql_native_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
