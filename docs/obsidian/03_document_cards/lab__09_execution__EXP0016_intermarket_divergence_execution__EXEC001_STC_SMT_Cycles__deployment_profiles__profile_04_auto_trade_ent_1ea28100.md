---
title: "Profile 04 — Auto Trade Entry Only Rehearsal"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_04_auto_trade_entry_only_rehearsal.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1074"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# Profile 04 — Auto Trade Entry Only Rehearsal

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_04_auto_trade_entry_only_rehearsal|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_04_auto_trade_entry_only_rehearsal.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1074` bytes

## خلاصه

Controlled real-entry rehearsal without real partial or hard-close automation. This is not the final production profile. It is a bridge between Paper Live and Full Managed Auto Trade. Runtime mode: Auto Trade. Enable: Broker position manager. Real auto-entry. Disable: Real partial close. Real hard close finalizer. Use the smallest practical risk while validating live order behavior. The operator should verify: 1. Real entries occur only on confirmed STC signals. 2. Real entry does not occur after the grace window. 3. Orders are sent only on Symbol1/Symbol2. 4. Orders carry the configured magic number. 5. SL and TP match the paper plan. 6. Split orders are capped and audited. 7. Max three ent

## Headings

- Profile 04 — Auto Trade Entry Only Rehearsal
-   Intent
-   Required mode
-   Required real transport
-   Risk recommendation
-   What to verify
-   Warning

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit|Profile 01 — Research Backtest Full Audit]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer|Profile 02 — Paper Live Observer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_03_paper_live_broker_audit|Profile 03 — Paper Live Broker Audit]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_05_auto_trade_full_managed|Profile 05 — Auto Trade Full Managed]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_06_emergency_hard_close_only|Profile 06 — Emergency Hard Close Only]] — `experiment`
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
