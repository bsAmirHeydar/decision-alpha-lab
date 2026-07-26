---
title: "Visual Replay Protocol"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/ui/VISUAL_REPLAY_PROTOCOL.md"
source_ext: ".md"
category: "ui_docs"
source_size_bytes: "5693"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Visual Replay Protocol

**Source:** [[docs/ui/VISUAL_REPLAY_PROTOCOL|docs/ui/VISUAL_REPLAY_PROTOCOL.md]]

**Category:** `ui_docs`  
**Status:** ok  
**Size:** `5693` bytes

## خلاصه

The Visual Replay Protocol defines how the UI replays market candles and overlays research artifacts on top of them. The goal is to make every test visually inspectable as if it were running live. The replay view is controlled by one object: A replay session contains: Valid replay states: 1. The chart must advance by candle index, not wall-clock time. 2. The current replay candle is the latest candle visible to the simulated system. 3. No visual object may appear before its `visible_from_index`. 4. L-rule nodes must become visible only after confirmation. 5. Metric events must become visible only when their event lifecycle reaches the current replay index. 6. Historical completed events may

## Headings

- Visual Replay Protocol
-   Purpose
-   Central Concept
-   Replay Status
-   Timeline Rules
-   Core Replay Controls
-   Chart Layout
-   Visual Layers
-   Selection Model
-   Hover Model
-   Candle Replay Semantics
-   M0001 Replay Behavior

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/ui/ROADMAP|UI Implementation Roadmap]] — `ui_docs`
- [[docs/ui/VISUALIZATION_API|Visualization API Contract]] — `ui_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/atomic_live_research_contract|Atomic Live Research Contract]] — `core_docs`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
