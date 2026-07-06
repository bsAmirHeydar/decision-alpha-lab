---
title: "M0001 Hunt Zone Origin From Node"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "990"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Hunt Zone Origin From Node

**Source:** [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `990` bytes

## خلاصه

Live hunt/territory rectangles now start from the original structural node time, not from `active_from_time`. Before: Now: The rectangle still extends to: or, for invalidated nodes when enabled: The visual audit should show the full territory relationship from the node origin. The node itself remains the structural anchor, while `active_from_time` remains the live-safe confirmation point used by the logic. This is a visual-origin change only. The detector still confirms nodes using the L-rule: The M0001 logic still uses confirmed nodes only. The rectangle simply begins at the node candle to make the territory's structural origin visually clear. `M0001_LiveVisualLab.mq5` version: `1.21`.

## Headings

- M0001 Hunt Zone Origin From Node
-   Change
-   Why
-   Important
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001 Extreme and Live Hunt Zone Audit]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_NODE_VISIBILITY_DIAGNOSTICS|M0001 Node Visibility Diagnostics]] — `mql_native_docs`
- [[docs/mql_native/M0001_TWO_MODE_CONSUMPTION|M0001 Two-Mode Node Consumption]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
