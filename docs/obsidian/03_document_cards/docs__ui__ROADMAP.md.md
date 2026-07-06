---
title: "UI Implementation Roadmap"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/ui/ROADMAP.md"
source_ext: ".md"
category: "ui_docs"
source_size_bytes: "4031"
entities:
  - "EXP0001"
  - "H0001"
  - "H0002"
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# UI Implementation Roadmap

**Source:** [[docs/ui/ROADMAP|docs/ui/ROADMAP.md]]

**Category:** `ui_docs`  
**Status:** ok  
**Size:** `4031` bytes

## خلاصه

Build the UI as a professional research terminal in layers. Do not start by drawing every possible feature. Start by building the central replay engine and typed visualization API. Deliverables: `docs/ui/README.md` `docs/ui/ARCHITECTURE.md` `docs/ui/FOLDER_STRUCTURE.md` `docs/ui/VISUAL_REPLAY_PROTOCOL.md` `docs/ui/VISUALIZATION_API.md` `docs/ui/ROADMAP.md` `apps/README.md` `apps/api/README.md` `apps/web/README.md` Definition of done: UI purpose is clear. Research/UI boundary is clear. Replay behavior is specified. Visualization contract is metric-agnostic. Folder structure is agreed before code is written. Goal: Expose existing research data to the UI without changing the lab engine. Endpoin

## Headings

- UI Implementation Roadmap
-   Strategy
-   Phase 0 — Architecture Freeze
-   Phase 1 — Backend Read API
-   Phase 2 — Frontend Shell
-   Phase 3 — Market Replay Core
-   Phase 4 — M0001 Visual Adapter
-   Phase 5 — Research Lineage Browser
-   Phase 6 — Experiment and Validation Workbench
-   Phase 7 — Live Monitor Mode

## Entities

`EXP0001`, `H0001`, `H0002`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/ui/VISUALIZATION_API|Visualization API Contract]] — `ui_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/ui/VISUAL_REPLAY_PROTOCOL|Visual Replay Protocol]] — `ui_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
