---
title: "M0001 LogRTV Random Null Comparison"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1644"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
---


# M0001 LogRTV Random Null Comparison

**Source:** [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1644` bytes

## خلاصه

Raw RTV is useful for interpretation, but it is naturally bounded below and unbounded above. Statistical comparison is therefore done on: This makes a 2x expansion and a 0.5x contraction symmetric: The node sample uses final M0001 events only: For every ready node event, a matched random reference window is generated: This creates a parallel random baseline using the same measurement structure. All extra per-bar prints are disabled by default. The EA prints one compact line only when the node-vs-random logRTV result changes: The line contains: The huge multi-line distribution report and the standard per-bar status print are disabled. The compact result is throttled by signature, so it only p

## Headings

- M0001 LogRTV Random Null Comparison
-   Purpose
-   Node sample
-   Random null sample
-   Journal output
-   Performance
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_LATEST_VISUAL_CAPS|M0001 Latest Visual Caps]] — `mql_native_docs`
- [[docs/mql_native/M0001_PROJECT_REPORT_SYNC|M0001 Project Report Sync]] — `mql_native_docs`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001 RTV — Log High/Low Volatility]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
