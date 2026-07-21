---
title: "LEVEL 03 — STC SMT Check Candle Aggregator"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "729"
entities:
  - "EXEC001"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# LEVEL 03 — STC SMT Check Candle Aggregator

**Source:** [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `729` bytes

## خلاصه

This document mirrors the implementation-level notes for: `docs/evidence/level_03_check_candle_aggregator_pair_data_completeness/dad06b849807_24_level_03_check_candle_aggregator.md` Level 03 adds the M1-based check-candle data layer for EXEC001 STC SMT Cycles. It does not add W levels, SMT detection, signal generation, paper trading, drawing, partial close, hard close, or auto trading. Generated Common Files outputs: `dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_build_sanity.csv` `dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_runtime_events.csv` `dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_time_audit.csv` `dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_check_candles.csv`

## Headings

- LEVEL 03 — STC SMT Check Candle Aggregator

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/level_03_check_candle_aggregator_pair_data_completeness/dad06b849807_24_level_03_check_candle_aggregator|Level 03 — Check Candle Aggregator and Pair Data Completeness]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|Level 06 STC SMT Candidate Engine]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|Level 08 STC SMT Risk Plan and Paper Entry]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL 09 — STC SMT Paper Outcome Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|Level 11 STC SMT Hard Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|Level 14 — STC SMT Paper Live Alerts]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL 18 — STC SMT Real Hard Close Finalizer]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|EXP0016 Intermarket Divergence Execution — Implementation Plan Index]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL 10 — STC SMT Partial Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER|LEVEL 17 — STC SMT Real Partial Close Manager]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
