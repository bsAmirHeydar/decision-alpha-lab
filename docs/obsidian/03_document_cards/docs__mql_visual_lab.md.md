---
title: "MQL5 Visual Lab Architecture"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_visual_lab.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "2631"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# MQL5 Visual Lab Architecture

**Source:** [[docs/mql_visual_lab|docs/mql_visual_lab.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `2631` bytes

## خلاصه

The React/FastAPI UI has been removed. The project now uses a cleaner split: M0001 is computed in Python from the same live-style candle-by-candle engine for: actual L-rule structural nodes random baseline reference points Python exports a simple CSV visual contract. MQL5 reads the CSV and draws objects directly on the MT5 chart. From the project root: With random baseline: Default output: Copy that CSV to your real terminal data folder: Copy the expert: to: Then compile it in MetaEditor and attach it to the same symbol/timeframe chart. The MQL expert has inputs for toggling: The research truth stays in Python, where it is testable and reproducible. The visual inspection happens in MT5/MQL5,

## Headings

- MQL5 Visual Lab Architecture
-   Core idea
-   Main files
-   Export example
-   Visual layers
-   Why this is cleaner
-   Live visual testing mode

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/mql_live_visual_lab|MQL5 Visual Lab: Python Brain, MT5 Eyes]] — `core_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
