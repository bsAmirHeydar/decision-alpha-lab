---
title: "H6 Fast Box Visualizer — Official Algorithm"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/H6_BOX_ALGORITHM_README.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "5225"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# H6 Fast Box Visualizer — Official Algorithm

**Source:** [[docs/debug/H6_BOX_ALGORITHM_README|docs/debug/H6_BOX_ALGORITHM_README.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `5225` bytes

## خلاصه

H6 does not compute touch, extreme, zone, revisit, or invalidation. It uses M0001 only: `DAL_DetectLRuleNodes` `DAL_M0001ComputeEvents` `event.territory_lower` `event.territory_upper` `event.entry_index` `event.exit_index` `event.touch_confirmed` By default, every confirmed M0001 event gets exactly one persistent box. This is intentionally broader than the old horizon-only logic so no touched/revisited event disappears just because it is below H1. Box vertical bounds are exactly M0001 territory: H6 does not rebuild zone geometry. Default: `InpH6BoxRightMode`: `0`: right edge = horizon candle `1`: right edge = M0001 event exit candle `2`: right edge = latest available bar Touch candle is zero

## Headings

- H6 Fast Box Visualizer — Official Algorithm
-   Source of truth
-   What gets drawn
-   Geometry
-   Time range
-   Color
-   Persistence
-   Execution
-   Performance
-   Release 141 — selectable zone projection mode
-     `DAL_M0006_ZONE_FULL_M0001_TERRITORY`
-     `DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE`

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
