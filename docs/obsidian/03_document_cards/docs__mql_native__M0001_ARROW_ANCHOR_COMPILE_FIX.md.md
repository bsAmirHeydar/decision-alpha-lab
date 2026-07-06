---
title: "M0001 Arrow Anchor Compile Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_ARROW_ANCHOR_COMPILE_FIX.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "535"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
---


# M0001 Arrow Anchor Compile Fix

**Source:** [[docs/mql_native/M0001_ARROW_ANCHOR_COMPILE_FIX|docs/mql_native/M0001_ARROW_ANCHOR_COMPILE_FIX.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `535` bytes

## خلاصه

MetaEditor can reject `ENUM_ARROW_ANCHOR` defaults when the constant name overlaps with text/object anchor constants. Error: The arrow helper now accepts the arrow anchor as `int` and passes it directly to `OBJPROP_ANCHOR`. This avoids enum-name ambiguity while keeping the same behavior: `M0001_LiveVisualLab.mq5` version: `1.14`.

## Headings

- M0001 Arrow Anchor Compile Fix
-   Problem
-   Fix
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001 Extreme and Live Hunt Zone Audit]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_NODE_RANDOM_REPORTS|M0001 Final Node/Random Reports]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/mql_native/M0001_HARD_CLEAN_VISUAL|M0001 Hard Clean Visual]] — `mql_native_docs`
- [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|M0001 Hunt Zone Origin From Node]] — `mql_native_docs`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_LATEST_VISUAL_CAPS|M0001 Latest Visual Caps]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
