---
title: "Quant Lab UI Architecture"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/ui/README.md"
source_ext: ".md"
category: "ui_docs"
source_size_bytes: "3436"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Quant Lab UI Architecture

**Source:** [[docs/ui/README|docs/ui/README.md]]

**Category:** `ui_docs`  
**Status:** ok  
**Size:** `3436` bytes

## خلاصه

The Quant Lab UI is the visual operating system for Decision Alpha Lab. It is not a decorative dashboard. It is the research cockpit where observations, hypotheses, experiments, metrics, validations, production signals, and execution evidence become visible and inspectable. The UI must make the full research chain transparent: Every visual object must be traceable back to the research object that produced it. The UI must never become the research engine. The Python lab remains the source of truth for: market data structural nodes metrics experiments validations reports execution logs The UI only visualizes, navigates, inspects, and controls approved research workflows through explicit APIs.

## Headings

- Quant Lab UI Architecture
-   Purpose
-   Core Principle
-   Product Vision
-   Non-Negotiable Requirements
-   Recommended Stack
-   Design Boundary
-   Document Map

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/ui/ROADMAP|UI Implementation Roadmap]] — `ui_docs`
- [[docs/ui/VISUAL_REPLAY_PROTOCOL|Visual Replay Protocol]] — `ui_docs`
- [[docs/ui/VISUALIZATION_API|Visualization API Contract]] — `ui_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
