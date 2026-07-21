---
title: "02 - Normalized Strategy Specification"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "8595"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Validation"
---


# 02 - Normalized Strategy Specification

**Source:** [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `8595` bytes

## خلاصه

Strategy ID: `EXEC001_STC_SMT_CYCLES` Strategy family: Intermarket divergence execution. Primary signal type: SMT divergence between two index symbols. Default symbols: Symbol1: `SPXUSD` Symbol2: `NDXUSD` The same logic applies to equivalent pairs such as `SPX/NDX`, `US500/NAS100`, `ES/NQ`, or broker-specific equivalents. The code must treat `Symbol1` and `Symbol2` as both data symbols and execution symbols for this strategy version. The EA may be attached to any chart. The chart symbol does not define the strategy universe. All analysis and execution use only `Symbol1` and `Symbol2`. The EA must block duplicate active instances for the same strategy ID and symbol pair. This prevents double

## Headings

- 02 - Normalized Strategy Specification
-   1. Strategy identity
-   2. Runtime independence
-   3. Trading day
-   4. M cycles and no-entry gaps
-   5. W cycles
-   6. Reference matrix
-   7. Structural two-symbol comparison
-   8. Hunt definition
-   9. Side mapping
-   10. Confirmation
-   11. Check candle construction

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
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
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
