---
title: "EXP0015 CME/live/backtest implementation plan"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/EXP0015_cme_live_backtest_plan.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1747"
entities:
  - "EXP0015"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
---


# EXP0015 CME/live/backtest implementation plan

**Source:** [[docs/EXP0015_cme_live_backtest_plan|docs/EXP0015_cme_live_backtest_plan.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1747` bytes

## خلاصه

The project now separates the divergence engine from data acquisition. Implemented in this patch: MQL5 candle/session divergence engine. Python backtest runner. Broker data source mode. External CSV data source mode. Session reference levels. Candle reference levels. Step/lag/valid-window logic. Basic MFE/MAE/return outcome columns. Implemented as a stable bridge boundary: `tools/cme_bridge/dal_cme_bridge.py` `serve` mode for localhost HTTP bars. `live_csv_tail` mode for MT5 Common Files. The bridge accepts legally obtained CME or CME-sourced data and normalizes it into DAL candle CSVs. Direct CME/vendor adapters should be added inside this bridge, not inside MQL5. To activate direct CME/ven

## Headings

- EXP0015 CME/live/backtest implementation plan
-   Stage 1: source-agnostic divergence engine
-   Stage 2: live data bridge
-   Stage 3: direct CME/vendor adapter
-   Stage 4: live MQL5 monitor
-   Stage 5: next upgrades

## Entities

`EXP0015`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]

## Related documents

- [[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|EXP0015 Legacy Compile Fix]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[tools/cme_bridge/README|DAL CME Bridge for EXP0015]] — `tool_docs`
- [[docs/EXP0015_cme_live_provider_patch|EXP0015 CME Live Provider Patch]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|EXP0015 Intermarket Candle + Session Divergence]] — `experiment`
- [[mql5/Experts/IntermarketDivergence/README|Intermarket Divergence Experts]] — `mql5_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_visual_lab|MQL5 Visual Lab Architecture]] — `core_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
