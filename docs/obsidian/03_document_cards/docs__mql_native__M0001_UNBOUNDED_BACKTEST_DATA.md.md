---
title: "M0001 Unbounded Backtest Data"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_UNBOUNDED_BACKTEST_DATA.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1220"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# M0001 Unbounded Backtest Data

**Source:** [[docs/mql_native/M0001_UNBOUNDED_BACKTEST_DATA|docs/mql_native/M0001_UNBOUNDED_BACKTEST_DATA.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1220` bytes

## خلاصه

Backtests are no longer limited by an arbitrary candle count. Default: Meaning: If you want a rolling cap for performance, set: or any positive number. `DAL_AppendBarChronological()` now treats `max_bars <= 0` as unbounded. It keeps every newly closed candle in chronological order and does not drop old candles. This means Strategy Tester controls the sample using its own symbol/timeframe/date range, not the EA. `DAL_LoadBarsChronological()` also treats `requested_bars <= 0` as all available bars from `Bars(symbol, timeframe)`, instead of falling back to 500. Default computed event cap is now: Meaning unlimited computed events. Visual caps are also zero by default: Meaning draw all audit obje

## Headings

- M0001 Unbounded Backtest Data
-   Change
-   Live stream behavior
-   Fallback bulk loader
-   Computation limits
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_LATEST_VISUAL_CAPS|M0001 Latest Visual Caps]] — `mql_native_docs`
- [[docs/mql_native/M0001_PROJECT_REPORT_SYNC|M0001 Project Report Sync]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|MQL-Native Runtime Architecture]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
