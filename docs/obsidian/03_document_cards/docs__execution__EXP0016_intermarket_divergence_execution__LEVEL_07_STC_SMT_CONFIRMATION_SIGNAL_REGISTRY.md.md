---
title: "LEVEL 07 STC SMT Confirmation and Signal Registry"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "706"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# LEVEL 07 STC SMT Confirmation and Signal Registry

**Source:** [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `706` bytes

## خلاصه

Level 07 adds the first signal registry layer for `EXEC001_STC_SMT_Cycles`. It confirms Level 06 SMT candidates at the close of their check candle and writes consumed audit-only signal rows to: `dal/stc/EXEC001_STC_SMT_Cycles/stc_level07_signal_registry.csv` No paper trade and no real order is created in this level. Main rules: The signal exists only at the exact check-candle close. Entry OFF means audit-only and consumed. Missed/offline entry moments are never entered later. Final M check candles are not entry-eligible. Same-check buy and sell are forgotten. All signal rows are consumed to prevent duplicate or delayed entries.

## Headings

- LEVEL 07 STC SMT Confirmation and Signal Registry

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|Level 02 — STC Time Engine and Cycle Classifier]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL 03 — STC SMT Check Candle Aggregator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|Level 04 — W Level Builder]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|Level 05 — STC SMT Reference Matrix and Raw Hunt Detector]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|Level 06 STC SMT Candidate Engine]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|Level 08 STC SMT Risk Plan and Paper Entry]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL 09 — STC SMT Paper Outcome Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|Level 11 STC SMT Hard Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_12_STC_SMT_PERSISTENCE_RESTART_RECOVERY|Level 12 — STC SMT Persistence and Restart Recovery]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|Level 14 — STC SMT Paper Live Alerts]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_15_STC_SMT_BROKER_POSITION_MANAGER|Level 15 — STC SMT Broker Position Manager]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
