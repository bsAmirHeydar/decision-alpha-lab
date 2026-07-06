---
title: "M0001 Python Brain / MQL Input Bridge"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_MQL_INPUT_PARAMETER_BRIDGE.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "2791"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Python Brain / MQL Input Bridge

**Source:** [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|docs/M0001_MQL_INPUT_PARAMETER_BRIDGE.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `2791` bytes

## خلاصه

M0001 must have one metric brain. Python is the only source of truth for: L-rule reference extraction reference point normalization territory construction entry/exit state machine before/inside samples RTV calculation hunt detection random baseline generation visual contract generation MQL5 is a visual terminal only. The practical issue is that parameter changes must still feel native inside MT5. This bridge solves that without duplicating the brain. The code being tested is the code producing the chart output. MQL does not recompute the metric. Recommended defaults: 1. Attach `M0001_LiveVisualLab.mq5` to an MT5 chart. 2. Set the Python brain parameters inside the Expert inputs. 3. Start the

## Headings

- M0001 Python Brain / MQL Input Bridge
-   Purpose
-   Architecture
-   Important MQL inputs
-     Python brain parameters
-     Bridge controls
-   How to run
-   Why this is strict
-   Validation mindset

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001 Parquet Event Bridge]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/mql_visual_lab|MQL5 Visual Lab Architecture]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
