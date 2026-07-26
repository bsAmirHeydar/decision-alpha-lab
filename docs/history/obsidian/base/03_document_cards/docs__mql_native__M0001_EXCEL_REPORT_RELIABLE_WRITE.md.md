---
title: "M0001 Reliable Excel Report Writing"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_EXCEL_REPORT_RELIABLE_WRITE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "908"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "MQL Native"
  - "Validation"
---


# M0001 Reliable Excel Report Writing

**Source:** [[docs/mql_native/M0001_EXCEL_REPORT_RELIABLE_WRITE|docs/mql_native/M0001_EXCEL_REPORT_RELIABLE_WRITE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `908` bytes

## خلاصه

Excel report writing now creates missing folders before `FileOpen` and prints success/failure messages to the Experts log. `InpExcelReportUseFullHistorySnapshot=true` writes a report-only CopyRates snapshot for full-history validation. It does not affect the live-stream engine or trading logic. This is useful when: because the runtime stream can be empty at init while a full report is still needed for research validation. In Strategy Tester, MetaTrader writes files under the tester agent sandbox, not always the normal terminal `MQL5\Files` folder. `M0001_LiveVisualLab.mq5` version: `1.34`.

## Headings

- M0001 Reliable Excel Report Writing
-   Fix
-   Inputs
-   Output
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_PROJECT_REPORT_SYNC|M0001 Project Report Sync]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
