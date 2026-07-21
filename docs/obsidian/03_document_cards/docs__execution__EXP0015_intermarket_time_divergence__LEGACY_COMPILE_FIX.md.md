---
title: "EXP0015 Legacy Compile Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "1908"
entities:
  - "EXP0015"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "NDS Anatomy"
---


# EXP0015 Legacy Compile Fix

**Source:** [[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `1908` bytes

## خلاصه

This patch fixes compile errors triggered by the deprecated expert: `mql5/Experts/IntermarketDivergence/IMD001_SPX_NDX_TimeDivergence.mq5` `mql5/Include/IntermarketDivergence/DAL_IMDReferenceLevels.mqh` The project had two EXP0015 API generations mixed together: 1. The current simple candle/session engine uses `IMD_*` types: `IMD_LevelFamily` `IMD_TriggerMode` `IMD_Event` 2. The deprecated SPX/NDX expert and old reference-level module used older `DAL_IMD*` names: `DAL_IMDLevelSide` `DAL_IMDLevelSource` `DAL_IMDTriggerMode` `DAL_IMDReferenceLevel` MetaEditor therefore reported errors such as `declaration without type`, `side - comma expected`, and undeclared `IMD_LEVEL_HIGH` or `IMD_LEVEL_L_N

## Headings

- EXP0015 Legacy Compile Fix
-   Cause
-   What the fix does
-   Recommended compile target
-   Important limitation

## Entities

`EXP0015`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[tools/cme_bridge/README|DAL CME Bridge for EXP0015]] — `tool_docs`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015 CME/live/backtest implementation plan]] — `core_docs`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|EXP0015 Intermarket Candle + Session Divergence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/EXP0015_cme_live_provider_patch|EXP0015 CME Live Provider Patch]] — `core_docs`
- [[mql5/Experts/IntermarketDivergence/README|Intermarket Divergence Experts]] — `mql5_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|EXP0016 Intermarket Divergence Execution — Implementation Plan Index]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL 10 — STC SMT Partial Close Simulator]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
