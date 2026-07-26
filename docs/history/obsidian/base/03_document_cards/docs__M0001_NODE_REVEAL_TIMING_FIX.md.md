---
title: "M0001 Node Reveal Timing Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_NODE_REVEAL_TIMING_FIX.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1025"
entities:
  - "M0001"
concepts:
  - "NDS Anatomy"
  - "Validation"
---


# M0001 Node Reveal Timing Fix

**Source:** [[docs/M0001_NODE_REVEAL_TIMING_FIX|docs/M0001_NODE_REVEAL_TIMING_FIX.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1025` bytes

## خلاصه

In a live-safe L-rule detector, a node located at candle `i` is not knowable at candle `i`. It becomes knowable only after `L` right-side candles exist: If the visual marker is always drawn back on `node_index`, the chart can feel like it is backpainting: the marker appears late but is placed on the older pivot candle. The Python visual contract now sends both times for every node: The MQL visual terminal can choose how to draw node markers: Default is `1`, which matches live decision semantics: the marker appears at the time the node becomes knowable. The node price remains the original Python node price in both modes. Only the marker time changes.

## Headings

- M0001 Node Reveal Timing Fix
-   Problem
-   Fix
-   Important

## Entities

`M0001`

## Concepts

- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX|M0001 Live Past-Only Event Bridge Fix]] — `core_docs`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001 Node Arrow Tip Anchor Fix]] — `core_docs`
- [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|M0001 Node Marker Precision and Bridge Performance Fix]] — `core_docs`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001 Parquet Event Bridge]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
