---
title: "MQL5 Visual Lab: Python Brain, MT5 Eyes"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_live_visual_lab.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1488"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# MQL5 Visual Lab: Python Brain, MT5 Eyes

**Source:** [[docs/mql_live_visual_lab|docs/mql_live_visual_lab.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1488` bytes

## خلاصه

MQL5 is now a visual-only layer. The metric brain is Python: The MT5 expert reads the Python-generated CSV visual contract: and draws it on the chart. Despite the name `LiveVisualLab`, the expert does not compute live logic. It reloads the Python visual contract on a timer and redraws it. This keeps research, tests, backtest artifacts and live visual inspection on one code path. Compile: Attach it to the same symbol/timeframe chart and set: All manual visual toggles are false by default. Use presets or turn on layers one by one.

## Headings

- MQL5 Visual Lab: Python Brain, MT5 Eyes
-   Main expert
-   Run Python brain once
-   Run Python brain continuously
-   Compile and attach MQL
-   Read more

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/mql_visual_lab|MQL5 Visual Lab Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_COMMON_FILES_SYNC_FIX|M0001 Common Files Sync Fix]] — `core_docs`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001 Parquet Event Bridge]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
