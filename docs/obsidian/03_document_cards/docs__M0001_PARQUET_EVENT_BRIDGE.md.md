---
title: "M0001 Parquet Event Bridge"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_PARQUET_EVENT_BRIDGE.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "2150"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Parquet Event Bridge

**Source:** [[docs/M0001_PARQUET_EVENT_BRIDGE|docs/M0001_PARQUET_EVENT_BRIDGE.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `2150` bytes

## خلاصه

The M0001 research brain must stay in Python, and all durable research artifacts should be stored as Parquet. MQL5 cannot read or write Parquet natively without external DLLs. Therefore the architecture is: The CSV render adapter is not the research artifact. It exists only because MQL can read simple text files natively. Python writes these on every bridge cycle: These are the files to use for: research replay validation journal Python/MQL visual audit reproducibility future reports strategy decision logs MQL still consumes: This file is only a drawing contract. It should not be used as the source of truth. Attach the Expert: Recommended MQL inputs: Then run the Python watcher: The status p

## Headings

- M0001 Parquet Event Bridge
-   Why
-   Authoritative Parquet artifacts
-   MQL render adapter
-   Run
-   Status

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/mql_visual_lab|MQL5 Visual Lab Architecture]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
