---
title: "M0001 Live Zone Resync"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_LIVE_ZONE_RESYNC.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1346"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 Live Zone Resync

**Source:** [[docs/mql_native/M0001_LIVE_ZONE_RESYNC|docs/mql_native/M0001_LIVE_ZONE_RESYNC.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1346` bytes

## خلاصه

The visible zone box must not freeze while the node is still alive. Pending-touch/event geometry is intentionally frozen for exit-gap confirmation, but the active live zone should continue to follow the latest expansion extreme. For every alive node: The pending event zone remains frozen internally for touch confirmation only: After a confirmed revisit in HUNT mode: So the current live box does not stretch from the original node origin after a confirmed revisit. `DAL_DrawRectangle` now upserts geometry. If a rectangle already exists, both anchor points are moved explicitly: This prevents stale rectangle coordinates if the same object name is reused. `M0001_LiveVisualLab.mq5` version: `1.45`.

## Headings

- M0001 Live Zone Resync
-   Problem
-   Fix
-   Revisit cycles
-   Renderer safety
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001 Extreme and Live Hunt Zone Audit]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|M0001 Hunt Zone Origin From Node]] — `mql_native_docs`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS|M0001 Node-Origin Zones and Revisit Text Colors]] — `mql_native_docs`
- [[docs/mql_native/M0001_NODE_VISIBILITY_DIAGNOSTICS|M0001 Node Visibility Diagnostics]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
