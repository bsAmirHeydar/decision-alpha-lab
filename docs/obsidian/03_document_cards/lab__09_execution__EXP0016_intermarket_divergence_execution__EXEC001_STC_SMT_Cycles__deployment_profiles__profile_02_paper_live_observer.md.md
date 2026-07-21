---
title: "Profile 02 — Paper Live Observer"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/profile_02_paper_live_observer/a5ba94007b51_profile_02_paper_live_observer.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "853"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# Profile 02 — Paper Live Observer

**Source:** [[docs/evidence/profile_02_paper_live_observer/a5ba94007b51_profile_02_paper_live_observer|docs/evidence/profile_02_paper_live_observer/a5ba94007b51_profile_02_paper_live_observer.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `853` bytes

## خلاصه

Run the live STC logic without broker interaction. Runtime mode: Paper Live. Disabled: Real auto-entry. Real partial close. Real hard close finalizer. Broker close actions. Broker position manager should normally be off in this profile. Enable: signal alerts; paper entry alerts; paper outcome alerts; partial paper alerts; hard close paper alerts; ambiguity alerts. Disable replay-on-init unless debugging. Drawing should normally be enabled so that the operator can visually compare: M/W boundaries; W high/low levels; check candle state; entry/SL/TP; partial and hard close markers. This profile passes when live alerts match the CSV rows and no real broker action occurs.

## Headings

- Profile 02 — Paper Live Observer
-   Intent
-   Required mode
-   Real transports
-   Alerts
-   Drawing
-   Acceptance criteria

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/profile_01_research_backtest_full_audit/b8f8aeb71c39_profile_01_research_backtest_full_audit|Profile 01 — Research Backtest Full Audit]] — `experiment`
- [[docs/evidence/profile_03_paper_live_broker_audit/b34ade2da6c9_profile_03_paper_live_broker_audit|Profile 03 — Paper Live Broker Audit]] — `experiment`
- [[docs/evidence/profile_04_auto_trade_entry_only_rehearsal/69b400182ebf_profile_04_auto_trade_entry_only_rehearsal|Profile 04 — Auto Trade Entry Only Rehearsal]] — `experiment`
- [[docs/evidence/profile_05_auto_trade_full_managed/39e8f73f460d_profile_05_auto_trade_full_managed|Profile 05 — Auto Trade Full Managed]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`
- [[docs/evidence/profile_06_emergency_hard_close_only/e564656d4633_profile_06_emergency_hard_close_only|Profile 06 — Emergency Hard Close Only]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|Level 02 — STC Time Engine and Cycle Classifier]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL 03 — STC SMT Check Candle Aggregator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|Level 04 — W Level Builder]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|Level 05 — STC SMT Reference Matrix and Raw Hunt Detector]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|Level 06 STC SMT Candidate Engine]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY|LEVEL 07 STC SMT Confirmation and Signal Registry]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
