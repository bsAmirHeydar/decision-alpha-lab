---
title: "E0006 — Revisit Secondary-Node Entry and Stop Anchors"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "3926"
entities:
  - "E0006"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0006 — Revisit Secondary-Node Entry and Stop Anchors

**Source:** [[docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README|docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `3926` bytes

## خلاصه

This document defines the third stop-anchor mode and the second revisit-entry mode added after the original E0006 execution design. In the first E0006 revisit model, the origin node stays the main execution anchor: The new model treats the first touch as a structural event that can create a smaller same-side node. On the next revisit, execution can be transferred from the large origin node to this smaller node. For a BUY example: For SELL, the logic is symmetric with HIGH nodes. Available revisit entry anchors: Available stop anchors: The secondary-node modes require `InpOnlyTradeRevisitZones = true` because there is no first-touch secondary node before the first touch exists. This is the or

## Headings

- E0006 — Revisit Secondary-Node Entry and Stop Anchors
-   Why this mode exists
-   Inputs
-   Revisit entry mode 1 — origin zone
-   Revisit entry mode 2 — secondary-node zone
-   Stop mode 1 — origin zone back
-   Stop mode 2 — origin node
-   Stop mode 3 — revisit secondary node
-   Recommended secondary-node revisit experiment

## Entities

`E0006`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[docs/debug/E0007/README|E0007 — Purple Source Extreme Executor Template]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/E0009/README|E0009 — Reversal Macro / Latest Setup / Hook Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[lab/03_validation/VAL0006_h5_live_touch_replay/README|VAL0006 — H5 live-valid touch-entry replay]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
