---
title: "M0001 Single-Source Live Architecture"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "4318"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Single-Source Live Architecture

**Source:** [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `4318` bytes

## خلاصه

M0001 has one brain only: The MQL expert does not compute nodes, territories, events, RTV, hunts, random baselines, or validation logic. It reads the visual contract produced by Python and draws it on the MT5 chart. The lab is intentionally designed around one obsessive rule: There must not be a separate MQL implementation of the metric and a separate Python implementation of the metric. Two engines create a hidden risk: the visual chart can look correct while the research engine is different, or the backtest can pass while the live visual logic is not the same. The same Python modules are used by every mode: These modules feed: MQL is allowed to: MQL is not allowed to: The live behavior is

## Headings

- M0001 Single-Source Live Architecture
-   Core decision
-   Why this matters
-   Runtime flow
-   Single-source invariant
-   What MQL is allowed to do
-   Live-like behavior without two engines
-   Debug packages
-   Validation philosophy
-   Professional framing
-   Anti-pattern avoided

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001 Event Bridge Architecture]] — `core_docs`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001 Python Brain / MQL Input Bridge]] — `core_docs`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL Live Visual Lab — All-in-One Apply]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL-Native Migration Decision]] — `core_docs`
- [[docs/mql_visual_lab|MQL5 Visual Lab Architecture]] — `core_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
