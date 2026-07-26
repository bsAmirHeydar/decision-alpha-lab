---
title: "M0001 Pending Touch and Hunt Priority"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_PENDING_TOUCH_HUNT_PRIORITY.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1081"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 Pending Touch and Hunt Priority

**Source:** [[docs/mql_native/M0001_PENDING_TOUCH_HUNT_PRIORITY|docs/mql_native/M0001_PENDING_TOUCH_HUNT_PRIORITY.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1081` bytes

## خلاصه

A zone touch is not immediately a confirmed TOUCH consumption. It is first a pending touch / active event. During this pending event, the node can still be hunted. HUNT always has priority over TOUCH while a touch event is pending. For a LOW node: For a HIGH node: TOUCH is confirmed only after: using the frozen event territory from the first touch candle. This keeps the state machine faithful to the intended model: `M0001_LiveVisualLab.mq5` version: `1.31`.

## Headings

- M0001 Pending Touch and Hunt Priority
-   Correction
-   Priority
-   TOUCH confirmation
-   Why
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
- [[docs/mql_native/M0001_LIVE_ZONE_RESYNC|M0001 Live Zone Resync]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS|M0001 Node-Origin Zones and Revisit Text Colors]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
