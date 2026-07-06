---
title: "M0001 Final Node/Random Reports"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_FINAL_NODE_RANDOM_REPORTS.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "887"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
---


# M0001 Final Node/Random Reports

**Source:** [[docs/mql_native/M0001_FINAL_NODE_RANDOM_REPORTS|docs/mql_native/M0001_FINAL_NODE_RANDOM_REPORTS.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `887` bytes

## خلاصه

The compact logRTV node-vs-random report is no longer printed during every runtime update. It is printed only when the EA finishes (`OnDeinit`). At the end of the run, exactly two final result prints are produced: The first line is the aggregate for final node/territory events. The second line is the aggregate for matched random reference windows, plus the node-vs-random comparison summary. The following are disabled by default: `M0001_LiveVisualLab.mq5` version: `1.55`.

## Headings

- M0001 Final Node/Random Reports
-   Purpose
-   Journal output
-   Disabled noisy prints
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_ARROW_ANCHOR_COMPILE_FIX|M0001 Arrow Anchor Compile Fix]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001 Extreme and Live Hunt Zone Audit]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/mql_native/M0001_HARD_CLEAN_VISUAL|M0001 Hard Clean Visual]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
