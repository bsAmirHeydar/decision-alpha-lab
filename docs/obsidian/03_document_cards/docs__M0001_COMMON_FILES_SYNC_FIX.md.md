---
title: "M0001 Common Files Sync Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_COMMON_FILES_SYNC_FIX.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1539"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
---


# M0001 Common Files Sync Fix

**Source:** [[docs/M0001_COMMON_FILES_SYNC_FIX|docs/M0001_COMMON_FILES_SYNC_FIX.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1539` bytes

## خلاصه

When the Expert is attached in MT5, MQL can write files into a different sandbox than the Python watcher is reading from, especially in Strategy Tester / Visual Mode. Typical symptom: The EA may actually be writing into tester/local file storage, not the same folder watched by Python. Use MetaQuotes Common Files as the bridge root. MQL input: Python watcher default: Shared root: Bridge files: Attach and compile: Set: Run Python: The PowerShell output should now watch:

## Headings

- M0001 Common Files Sync Fix
-   Problem
-   Fix
-   Run

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001 Parquet Event Bridge]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab|MQL5 Visual Lab: Python Brain, MT5 Eyes]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/mql_visual_lab|MQL5 Visual Lab Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
