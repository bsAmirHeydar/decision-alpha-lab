---
title: "M0001 Node Marker Precision and Bridge Performance Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1124"
entities:
  - "M0001"
concepts:
  - "NDS Anatomy"
---


# M0001 Node Marker Precision and Bridge Performance Fix

**Source:** [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1124` bytes

## خلاصه

The Python node price is the truth. The visual marker must point exactly to it. Wingdings arrow glyphs in MT5 can have confusing visual centers/anchors. To avoid glyph-anchor ambiguity, the default node marker is now a custom two-segment chevron: HIGH node: red `V` marker, exact vertex at node high, wings above the candle LOW node: green `^` marker, exact vertex at node low, wings below the candle Inputs: The exact chevron vertex is the Python node price. The bridge previously rewrote the runtime config on every timer cycle. That can cause Python to recompute the same candle stream repeatedly. Now the timer does not rewrite config unless explicitly requested: Normal flow:

## Headings

- M0001 Node Marker Precision and Bridge Performance Fix
-   Node marker
-   Performance

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX|M0001 Live Past-Only Event Bridge Fix]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001 Node Arrow Tip Anchor Fix]] — `core_docs`
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
