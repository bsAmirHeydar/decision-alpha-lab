---
title: "M0001 Extreme and Live Hunt Zone Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1285"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Extreme and Live Hunt Zone Audit

**Source:** [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1285` bytes

## خلاصه

After validating L-rule structural nodes, the next audit layer is expansion state: For LOW nodes: For HIGH nodes: The visual layer draws a dashed line: The live hunt zone is the current territory rectangle computed from the distance between the node price and the tracked expansion extreme. If the node has not been invalidated/hunted, the rectangle extends from `active_from_time` to the current live-stream bar. If the node is invalidated and `InpShowInvalidatedHuntZones=false`, no rectangle is drawn for it. The L-rule node detector is now exposed through: Downstream M0001 modules should use this stable facade and avoid modifying the validated detector internals.

## Headings

- M0001 Extreme and Live Hunt Zone Audit
-   Purpose
-   Inputs
-   Expansion extreme
-   Live hunt zone
-   Structural node module boundary

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
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|M0001 Hunt Zone Origin From Node]] — `mql_native_docs`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
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
