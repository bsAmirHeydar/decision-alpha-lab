---
title: "Profile 01 — Research Backtest Full Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1156"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# Profile 01 — Research Backtest Full Audit

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1156` bytes

## خلاصه

Historical validation with all audit outputs and no broker interaction. Runtime mode: Research Backtest. All real transports must be disabled: Real auto-entry: disabled. Broker position manager: disabled or harmless if only audit is needed. Real partial close: disabled. Real hard close finalizer: disabled. Paper Live real-action overrides: disabled. Enable: time audit; check candle audit; W level audit; hunt audit; SMT candidate audit; signal registry audit; paper entry audit; paper outcome audit; paper partial audit; paper hard close audit; persistence snapshot; validation reports. Alerts should not fire for historical backfill. The operator should review: validation summary; time audit; W

## Headings

- Profile 01 — Research Backtest Full Audit
-   Intent
-   Required mode
-   Real transports
-   Recommended audit settings
-   Expected output
-   Acceptance criteria

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL001/report|Report]] — `validation`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer|Profile 02 — Paper Live Observer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_03_paper_live_broker_audit|Profile 03 — Paper Live Broker Audit]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_04_auto_trade_entry_only_rehearsal|Profile 04 — Auto Trade Entry Only Rehearsal]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_05_auto_trade_full_managed|Profile 05 — Auto Trade Full Managed]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`
- [[lab/03_experiments/EXP0000_sample/report|Report]] — `experiment`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|Report]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
