
---
type: source_card
source_path: "tools/cme_bridge/README.md"
source_ext: ".md"
source_size: 13616
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Licensing", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0015"]
---

# Source Card — README.md

## Source

[[tools/cme_bridge/README|tools/cme_bridge/README.md]]

## Summary

This directory contains the data bridge used by **Decision Alpha Lab / EXP0015 Intermarket Divergence**. The goal is to give the MQL5 divergence engine clean ES/NQ-style futures bars for both: **Backtesting / offline research** from historical CME-sourced data. **Live monitoring** from a licensed real-time feed or a near-live historical polling workflow. The MQL5 expert stays source-agnostic. It only reads canonical CSV bars from MetaTrader Common Files. The bridge is responsible for obtaining, normalizing, storing, and copying those bars. This project does **not** bypass CME or vendor licensing. For true CME real-time data you need a legal market-data account, credentials, and the required exchange entitlements. The provided Databento provider expects `DATABENTO_API_KEY` and valid CME/Globex permissions. The Yah… Use this bridge only with data you are legally allowed to access and store

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0015

## Headings

- DAL CME Bridge for EXP0015
  - Important licensing boundary
  - Architecture
  - Files
    - Main entrypoints
  - Install
  - Set your Databento API key
  - Databento config
- Workflow A — Offline historical backtest
  - 1. Download historical ES/NQ bars
  - 2. Run the Python EXP0015 experiment
- Workflow B — Backtest inside MetaTrader 5 using external CSV

## Related Source Documents

- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|README.md]] — score `23`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `23`
- [[mql5/Experts/IntermarketDivergence/README|README.md]] — score `19`
- [[docs/flag_counting/README|README.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `18`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|README.md]] — score `18`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `18`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `18`
- [[mql5/Experts/IntermarketDivergenceExecution/README|README.md]] — score `18`
- [[tools/astro_live_bridge/README|README.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
