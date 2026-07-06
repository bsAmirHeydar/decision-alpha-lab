---
title: "Decision Alpha Lab project layout"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/PROJECT_LAYOUT.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1279"
concepts:
  - "Execution"
  - "MQL Native"
---


# Decision Alpha Lab project layout

**Source:** [[docs/PROJECT_LAYOUT|docs/PROJECT_LAYOUT.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1279` bytes

## خلاصه

This repository has one canonical root: The repository must **not** contain another tracked project copy under: All execution code, include files, and execution documentation must be edited in the canonical root paths above. A nested `decision-alpha-lab/` directory creates two competing source trees. That causes: patch context drift; MetaEditor compiling one copy while Git shows changes in another copy; duplicate include paths; stale execution modules surviving after a release update; false confidence that a fix was applied when the terminal is still reading the old file. If a nested project copy exists, back it up once, remove it, and commit the deletion: The backup zip is a temporary safet

## Headings

- Decision Alpha Lab project layout
-   Canonical source paths
-   Why nested project copies are banned
-   Cleanup rule

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015 CME/live/backtest implementation plan]] — `core_docs`
- [[docs/laboratory_architecture|Laboratory Architecture]] — `core_docs`
- [[docs/M0001_COMMON_FILES_SYNC_FIX|M0001 Common Files Sync Fix]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001 Parquet Event Bridge]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab|MQL5 Visual Lab: Python Brain, MT5 Eyes]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/mql_visual_lab|MQL5 Visual Lab Architecture]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
