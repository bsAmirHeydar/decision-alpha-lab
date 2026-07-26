---
title: "MQL-Native Migration Decision"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/MQL_NATIVE_MIGRATION_DECISION.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "3936"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# MQL-Native Migration Decision

**Source:** [[docs/MQL_NATIVE_MIGRATION_DECISION|docs/MQL_NATIVE_MIGRATION_DECISION.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `3936` bytes

## خلاصه

The Decision Alpha Lab project will migrate M0001 from a Python-brain / MQL-visual bridge architecture to a native MQL5 execution architecture. The previous Python implementation is preserved as an archived reference in the branch: Going forward, MQL5 will become the primary runtime for live logic, visual validation, strategy testing, and research iteration. The Python bridge achieved an important goal: it proved the core M0001 idea, clarified the event model, and produced a useful reference implementation. However, it introduced runtime problems that are unacceptable for this project’s current direction. The main issues were: 1. **Asynchronous execution lag** MT5 Strategy Tester advances th

## Headings

- MQL-Native Migration Decision
-   Summary
-   Why Python Is Being Removed From the Active Runtime
-   What Is Not Being Removed
-   New Direction
-   Archived Reference
-   Decision

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001 Parquet Event Bridge]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/mql_visual_lab|MQL5 Visual Lab Architecture]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
