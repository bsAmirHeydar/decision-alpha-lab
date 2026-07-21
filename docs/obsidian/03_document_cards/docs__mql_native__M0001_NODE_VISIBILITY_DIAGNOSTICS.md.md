---
title: "M0001 Node Visibility Diagnostics"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_NODE_VISIBILITY_DIAGNOSTICS.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1185"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Node Visibility Diagnostics

**Source:** [[docs/mql_native/M0001_NODE_VISIBILITY_DIAGNOSTICS|docs/mql_native/M0001_NODE_VISIBILITY_DIAGNOSTICS.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1185` bytes

## خلاصه

This adds an on-chart diagnostic summary to separate three different questions: 1. Is data limited? 2. Are structural nodes being computed? 3. Are visual caps hiding some computed nodes? The summary now shows: If `nodes` is large and `last_node` is recent, the detector is not capped. If `nodes` is large but `node_draw=latest 2/N`, the cap is visual only. If `last_node` is far behind the current chart time, the L-rule detector has not confirmed a newer structural node yet for the current `InpL`. `InpBars` remains the data cap: Visual caps are separate: `M0001_LiveVisualLab.mq5` version: `1.27`.

## Headings

- M0001 Node Visibility Diagnostics
-   Purpose
-   New input
-   Summary fields
-   Interpretation
-   Important
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001 Extreme and Live Hunt Zone Audit]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|M0001 Hunt Zone Origin From Node]] — `mql_native_docs`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_TWO_MODE_CONSUMPTION|M0001 Two-Mode Node Consumption]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
