---
title: "M0001 Event Bridge Architecture"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_EVENT_BRIDGE_ARCHITECTURE.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "3039"
entities:
  - "M0001"
concepts:
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Event Bridge Architecture

**Source:** [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|docs/M0001_EVENT_BRIDGE_ARCHITECTURE.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `3039` bytes

## خلاصه

M0001 must be live-like without creating two brains. The tested implementation, the research implementation, and the chart-inspected implementation must be the same Python code. MQL is not allowed to compute M0001. It only: exports market candles observed by MT5; writes input parameters; draws Python output; can later execute orders from Python decisions. The previous bridge only let MQL write parameters. Python still read cached candles. That was useful for research, but it did not feel synchronized with the visual chart. The event bridge uses the chart as the market-data trigger. When a new candle arrives, or optionally every tick, MQL sends the current candle stream to Python. Recommended

## Headings

- M0001 Event Bridge Architecture
-   Goal
-   Architecture
-   Why this is different from the old bridge
-   Important MQL inputs
-   Python watcher
-   Sync files
-   Validation rule

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `debug_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
