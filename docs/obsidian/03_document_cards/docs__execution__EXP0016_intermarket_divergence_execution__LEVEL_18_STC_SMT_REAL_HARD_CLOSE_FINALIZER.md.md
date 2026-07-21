---
title: "LEVEL 18 — STC SMT Real Hard Close Finalizer"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "676"
entities:
  - "EXEC001"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "Validation"
---


# LEVEL 18 — STC SMT Real Hard Close Finalizer

**Source:** [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `676` bytes

## خلاصه

Patch scope: add the final real broker hard-close layer for EXEC001 STC SMT Cycles. This level is disabled by default. When explicitly enabled, it retries closing only Symbol1/Symbol2 positions with the configured STC magic number after 15:30 New York. It audits every attempt and verifies whether positions remain after each close request. Main implementation file: `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_RealHardClose.mqh` Main EA: `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` Primary output: `dal/stc/EXEC001_STC_SMT_Cycles/stc_level18_real_hard_close_finalizer.csv`

## Headings

- LEVEL 18 — STC SMT Real Hard Close Finalizer

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|Level 11 STC SMT Hard Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|EXP0016 Intermarket Divergence Execution — Implementation Plan Index]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL 03 — STC SMT Check Candle Aggregator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|Level 06 STC SMT Candidate Engine]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|Level 08 STC SMT Risk Plan and Paper Entry]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL 09 — STC SMT Paper Outcome Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL 10 — STC SMT Partial Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|Level 14 — STC SMT Paper Live Alerts]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
