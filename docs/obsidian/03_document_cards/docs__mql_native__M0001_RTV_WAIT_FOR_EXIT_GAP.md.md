---
title: "M0001 RTV Waits for Exit-Gap Closure"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_RTV_WAIT_FOR_EXIT_GAP.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "964"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "Structural Nodes"
  - "Validation"
---


# M0001 RTV Waits for Exit-Gap Closure

**Source:** [[docs/mql_native/M0001_RTV_WAIT_FOR_EXIT_GAP|docs/mql_native/M0001_RTV_WAIT_FOR_EXIT_GAP.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `964` bytes

## خلاصه

RTV is calculated only after the event has actually closed by exit-gap: Any candle that intersects the frozen zone resets the outside counter. So HUNT-before-confirmation events can still exist for visual audit, but they are not included in RTV mean/median and are written as non-ready/n/a. After exit-gap closure: The final outside confirmation candles are not included in the inside volatility sample. `M0001_LiveVisualLab.mq5` version: `1.50`.

## Headings

- M0001 RTV Waits for Exit-Gap Closure
-   Rule
-   RTV-ready condition
-   Sample construction
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|MQL-Native Runtime Architecture]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
