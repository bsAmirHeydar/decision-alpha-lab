---
title: "07 - Test Plan"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "5371"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Validation"
---


# 07 - Test Plan

**Source:** [[docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan|docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `5371` bytes

## خلاصه

The test plan ensures the STC SMT Cycles implementation follows the locked specification before any live trading. Every test should be deterministic and should write expected vs actual values to a report. Test M assignment: 20:00 is M1. 01:59 is M1. 02:00 is gap. 02:59 is gap. 03:00 is M2. 08:59 is M2. 09:00 is gap. 09:29 is gap. 09:30 is M3. 15:29 is M3. 15:30 is hard close/reset. Test W assignment for every W in M1, M2, and M3. Test DST transition dates using New York time. For each check timeframe, verify aggregation starts at 20:00 New York. Examples: 10m: 20:00-20:10. 10m: 21:20-21:30. 15m: 20:00-20:15. 3m: 20:00-20:03. Verify that final check candles ending at M boundaries cannot enter

## Headings

- 07 - Test Plan
-   1. Purpose
-   2. Time and cycle tests
-   3. Check candle anchoring tests
-   4. W level tests
-   5. Reference matrix tests
-   6. Hunt tests
-   7. SMT divergence tests
-   8. Confirmation tests
-   9. Reference selection tests
-   10. Ambiguity tests
-   11. Risk tests

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`
- [[docs/evidence/14_backtest_live_runtime/c31f0574e3ec_14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
