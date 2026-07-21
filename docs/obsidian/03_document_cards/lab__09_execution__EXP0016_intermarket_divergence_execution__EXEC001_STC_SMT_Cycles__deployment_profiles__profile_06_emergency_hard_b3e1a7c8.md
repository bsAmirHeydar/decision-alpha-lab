---
title: "Profile 06 — Emergency Hard Close Only"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/profile_06_emergency_hard_close_only/e564656d4633_profile_06_emergency_hard_close_only.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "932"
concepts:
  - "Execution"
  - "Intermarket Divergence"
---


# Profile 06 — Emergency Hard Close Only

**Source:** [[docs/evidence/profile_06_emergency_hard_close_only/e564656d4633_profile_06_emergency_hard_close_only|docs/evidence/profile_06_emergency_hard_close_only/e564656d4633_profile_06_emergency_hard_close_only.md]]

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

- [[docs/evidence/exp0000_sample/58c8a635ff91_report|Report]] — `experiment`
- [[docs/evidence/exp0001_structural_highs_lows_importance/337872464ffa_report|Report]] — `experiment`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/evidence/val001/360462a17ab1_report|Report]] — `validation`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/evidence/profile_01_research_backtest_full_audit/b8f8aeb71c39_profile_01_research_backtest_full_audit|Profile 01 — Research Backtest Full Audit]] — `experiment`
- [[docs/evidence/profile_02_paper_live_observer/a5ba94007b51_profile_02_paper_live_observer|Profile 02 — Paper Live Observer]] — `experiment`
- [[docs/evidence/profile_03_paper_live_broker_audit/b34ade2da6c9_profile_03_paper_live_broker_audit|Profile 03 — Paper Live Broker Audit]] — `experiment`
- [[docs/evidence/profile_04_auto_trade_entry_only_rehearsal/69b400182ebf_profile_04_auto_trade_entry_only_rehearsal|Profile 04 — Auto Trade Entry Only Rehearsal]] — `experiment`
- [[docs/evidence/profile_05_auto_trade_full_managed/39e8f73f460d_profile_05_auto_trade_full_managed|Profile 05 — Auto Trade Full Managed]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
