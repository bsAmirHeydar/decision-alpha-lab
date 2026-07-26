---
title: "M0001 Live Past-Only Bridge Compile Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_LIVE_PAST_ONLY_COMPILE_FIX.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "577"
entities:
  - "M0001"
---


# M0001 Live Past-Only Bridge Compile Fix

**Source:** [[docs/M0001_LIVE_PAST_ONLY_COMPILE_FIX|docs/M0001_LIVE_PAST_ONLY_COMPILE_FIX.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `577` bytes

## خلاصه

The previous live past-only bridge snapshot accidentally inserted the `StatusValue` helper as escaped text (`\n`) on one physical MQL line. MetaEditor then parsed the whole block as invalid global tokens. Typical compile errors: `StatusValue()` is now emitted as normal MQL source code. The missing input `InpBridgeTimerConfigPulse` is also declared. Version: `6.51`.

## Headings

- M0001 Live Past-Only Bridge Compile Fix
-   Problem
-   Fix

## Entities

`M0001`

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_COMMON_FILES_SYNC_FIX|M0001 Common Files Sync Fix]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX|M0001 Live Past-Only Event Bridge Fix]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001 Node Arrow Tip Anchor Fix]] — `core_docs`
- [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|M0001 Node Marker Precision and Bridge Performance Fix]] — `core_docs`
- [[docs/M0001_NODE_REVEAL_TIMING_FIX|M0001 Node Reveal Timing Fix]] — `core_docs`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001 Parquet Event Bridge]] — `core_docs`
- [[docs/M0001_PARQUET_TYPE_SAFETY_FIX|M0001 Parquet Type Safety Fix]] — `core_docs`
- [[docs/M0001_REVERT_NODE_TIMING_FAST_SYNC|M0001 Revert Node Timing Mode and Fast Sync]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
