---
title: "M0001 Live Past-Only Event Bridge Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1090"
entities:
  - "M0001"
concepts:
  - "NDS Anatomy"
---


# M0001 Live Past-Only Event Bridge Fix

**Source:** [[docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX|docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1090` bytes

## خلاصه

1. Strategy Tester could show nodes from future candles if the bridge exported a count-based historical window rather than a time-bounded window. 2. MQL repeatedly deleted and redrew objects on every timer, causing flicker and overload. 3. Python could hit `PermissionError [WinError 32]` while refreshing the MQL CSV adapter while MT5 was reading it. MQL exports candles using a time-bounded `CopyRates(start_time, end_time)` call. `end_time` is the last closed bar when `InpBridgeClosedBarsOnly=true`. MQL redraws only when Python publishes a new `request_id` in the status file. MQL file handles use share flags. Python writes the visual adapter through a temp file and retries on Windows file loc

## Headings

- M0001 Live Past-Only Event Bridge Fix
-   Problems
-   Fixes
-   Important inputs

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001 Node Arrow Tip Anchor Fix]] — `core_docs`
- [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|M0001 Node Marker Precision and Bridge Performance Fix]] — `core_docs`
- [[docs/M0001_NODE_REVEAL_TIMING_FIX|M0001 Node Reveal Timing Fix]] — `core_docs`
- [[docs/M0001_PARQUET_TYPE_SAFETY_FIX|M0001 Parquet Type Safety Fix]] — `core_docs`
- [[docs/M0001_REVERT_NODE_TIMING_FAST_SYNC|M0001 Revert Node Timing Mode and Fast Sync]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab|MQL5 Visual Lab: Python Brain, MT5 Eyes]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
