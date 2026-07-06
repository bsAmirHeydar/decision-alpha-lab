---
title: "Profile 06 — Emergency Hard Close Only"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_06_emergency_hard_close_only.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "932"
concepts:
  - "Execution"
  - "Intermarket Divergence"
---


# Profile 06 — Emergency Hard Close Only

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_06_emergency_hard_close_only|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_06_emergency_hard_close_only.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `932` bytes

## خلاصه

Close remaining STC-managed positions after 15:30 New York without allowing new entries. Disable: STC entry. Real auto-entry. Real partial close. Enable: Broker position manager. Real hard close finalizer. The finalizer must only close positions that: 1. are on Symbol1 or Symbol2; 2. match the configured magic number; 3. are still open after the STC hard-close threshold. Manual or foreign positions must never be closed. Use this profile when: the EA was restarted after 15:30; managed positions remain open unexpectedly; auto-entry must stay disabled while cleanup is performed; the operator wants finalizer-only behavior. The profile passes when all matching magic-number positions are closed or

## Headings

- Profile 06 — Emergency Hard Close Only
-   Intent
-   Required behavior
-   Important constraints
-   Use cases
-   Acceptance criteria

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]

## Related documents

- [[lab/03_experiments/EXP0000_sample/report|Report]] — `experiment`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|Report]] — `experiment`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL001/report|Report]] — `validation`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit|Profile 01 — Research Backtest Full Audit]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer|Profile 02 — Paper Live Observer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_03_paper_live_broker_audit|Profile 03 — Paper Live Broker Audit]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_04_auto_trade_entry_only_rehearsal|Profile 04 — Auto Trade Entry Only Rehearsal]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_05_auto_trade_full_managed|Profile 05 — Auto Trade Full Managed]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
