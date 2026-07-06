---
title: "Intermarket Divergence Experts"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "mql5/Experts/IntermarketDivergence/README.md"
source_ext: ".md"
category: "mql5_docs"
source_size_bytes: "637"
entities:
  - "EXP0015"
concepts:
  - "Intermarket Divergence"
  - "MQL Native"
  - "Validation"
---


# Intermarket Divergence Experts

**Source:** [[mql5/Experts/IntermarketDivergence/README|mql5/Experts/IntermarketDivergence/README.md]]

**Category:** `mql5_docs`  
**Status:** ok  
**Size:** `637` bytes

## خلاصه

Batch expert for EXP0015. It scans two aligned symbols, usually S&P/US500 and Nasdaq/NAS100, and records time-step divergences between their highs/lows. The expert is intentionally not tick-driven. `OnTick()` is empty. In research mode the whole scan runs once in `OnInit()` and exports CSV files to Common Files. Default output: Turn on `InpWriteAllEvaluatedSteps` only when you need a full audit table for every compared high/low step. It can be large.

## Headings

- Intermarket Divergence Experts
-   IMD001_SPX_NDX_TimeDivergence

## Entities

`EXP0015`

## Concepts

- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|EXP0015 Intermarket Candle + Session Divergence]] — `experiment`
- [[tools/cme_bridge/README|DAL CME Bridge for EXP0015]] — `tool_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/IntermarketDivergenceExecution/README|Intermarket Divergence Execution Experts]] — `mql5_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution]] — `experiment`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0005_mql_native_directional_memory/README|EXP0005 — MQL-native H0005 directional memory]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
