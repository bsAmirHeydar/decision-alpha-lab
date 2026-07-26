---
title: "05 - Execution, Risk, Position Management, and Outcomes"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "6479"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Validation"
---


# 05 - Execution, Risk, Position Management, and Outcomes

**Source:** [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `6479` bytes

## خلاصه

Backtest: The strategy confirms at the close of a check candle. Entry price is the open of the next check candle. If there is no next check candle inside the same M, no entry is allowed. Live/paper: Entry is a market order immediately after the confirmation check candle closes. If the EA is offline at the exact entry time, no delayed entry is allowed. If Entry STC is ON, confirmed signals may execute. If Entry STC is OFF: The signal is audited. No trade is opened. The signal is consumed for trading. The strategy must not enter later if Entry STC is turned ON. Existing positions continue to be managed. The trade is always opened on the clean symbol that did not hunt. The strategy uses `Symbol

## Headings

- 05 - Execution, Risk, Position Management, and Outcomes
-   1. Entry model
-   2. Entry STC switch
-   3. Trade symbol
-   4. Stop loss
-   5. Target
-   6. Risk sizing
-   7. Broker volume limits
-   8. Order failure
-   9. Trade counter
-   10. Hedging OFF
-   11. Hedging ON

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
- [[docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan|07 - Test Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`
- [[docs/evidence/14_backtest_live_runtime/c31f0574e3ec_14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
