---
title: "DAL CME Bridge for EXP0015"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "tools/cme_bridge/README.md"
source_ext: ".md"
category: "tool_docs"
source_size_bytes: "13616"
entities:
  - "EXP0015"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
---


# DAL CME Bridge for EXP0015

**Source:** [[tools/cme_bridge/README|tools/cme_bridge/README.md]]

**Category:** `tool_docs`  
**Status:** ok  
**Size:** `13616` bytes

## خلاصه

This directory contains the data bridge used by **Decision Alpha Lab / EXP0015 Intermarket Divergence**. The goal is to give the MQL5 divergence engine clean ES/NQ-style futures bars for both: 1. **Backtesting / offline research** from historical CME-sourced data. 2. **Live monitoring** from a licensed real-time feed or a near-live historical polling workflow. The MQL5 expert stays source-agnostic. It only reads canonical CSV bars from MetaTrader Common Files. The bridge is responsible for obtaining, normalizing, storing, and copying those bars. This project does **not** bypass CME or vendor licensing. For true CME real-time data you need a legal market-data account, credentials, and the req

## Headings

- DAL CME Bridge for EXP0015
-   Important licensing boundary
-   Architecture
-   Files
-     Main entrypoints
-   Install
-   Set your Databento API key
-   Databento config
- Workflow A — Offline historical backtest
-   1. Download historical ES/NQ bars
-   2. Run the Python EXP0015 experiment
- Workflow B — Backtest inside MetaTrader 5 using external CSV

## Entities

`EXP0015`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|EXP0015 Intermarket Candle + Session Divergence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/IntermarketDivergence/README|Intermarket Divergence Experts]] — `mql5_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/IntermarketDivergenceExecution/README|Intermarket Divergence Execution Experts]] — `mql5_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
