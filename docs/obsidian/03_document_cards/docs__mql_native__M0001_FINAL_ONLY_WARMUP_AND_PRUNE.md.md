---
title: "M0001 Final-Only Research Report, Warmup, and MQL Prune"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1509"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Final-Only Research Report, Warmup, and MQL Prune

**Source:** [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1509` bytes

## خلاصه

Runtime distribution calculations were removed. During live-stream processing the EA only updates a lightweight runtime comment. The node-vs-random logRTV statistics are computed once in `OnDeinit`. A new input seeds the live stream with closed historical bars before the test/live stream begins: Warmup bars are used to reconstruct old structural nodes and their consumed/live state. The research sample is filtered by `analysis_start`, which is set to the first newly appended bar after warmup, so final reports include only events whose `entry_time >= analysis_start`. This allows old nodes to be available for touches inside the test period without contaminating the report with pre-test events.

## Headings

- M0001 Final-Only Research Report, Warmup, and MQL Prune
-   Final-only statistics
-   Warmup input
-   Random baseline fairness
-   Removed dead MQL files
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
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
