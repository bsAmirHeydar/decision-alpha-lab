---
title: "M0001 Candle-Gated Runtime"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_CANDLE_GATED_RUNTIME.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1496"
entities:
  - "M0001"
concepts:
  - "Convexity"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Candle-Gated Runtime

**Source:** [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|docs/mql_native/M0001_CANDLE_GATED_RUNTIME.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1496` bytes

## خلاصه

Version: 1.59 M0001 is still an Expert Advisor, so MetaTrader wakes it through `OnTick()`. The research engine itself is not tick-based. The timer is disabled by default: If a timer is enabled later, it must pass through the same candle gate. The optimized default is: This keeps runtime light while restoring final chart drawings. During the run the EA appends closed candles only. At shutdown, the same final computed state is used for both: `DAL_M0001_FINAL_NODES` / `DAL_M0001_FINAL_RANDOM` final node, zone, revisit, state, and optional RTV/event drawings For step-by-step visual debugging: This recomputes and redraws on each newly closed candle only. It never runs heavy logic on intra-candle

## Headings

- M0001 Candle-Gated Runtime
-   Runtime behavior
-   Fast default
-   Visual replay mode
-   Semantics unchanged

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001 Consumed Node Repair]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001 Extreme and Live Hunt Zone Audit]] — `mql_native_docs`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001 Fast Final-Only Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|M0001 Hunt Zone Origin From Node]] — `mql_native_docs`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
