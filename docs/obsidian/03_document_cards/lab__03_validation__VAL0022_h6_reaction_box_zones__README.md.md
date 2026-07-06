---
title: "VAL0022 — H6 Reaction Box Zones"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0022_h6_reaction_box_zones/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "13920"
entities:
  - "M0001"
  - "VAL0022"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# VAL0022 — H6 Reaction Box Zones

**Source:** [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|lab/03_validation/VAL0022_h6_reaction_box_zones/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `13920` bytes

## خلاصه

Goal: validate the H6 chart object logic where a node touch that confirms reversal creates a rectangle from node origin to touch location. Validation checklist: 1. `sampleCalls=0`, `branchSamplesBuilt=0`, `m0002Calls=0` remain unchanged. 2. `DAL_H0006_REACTION_BOX_AUDIT` is printed. 3. Boxes are drawn when `InpH6DrawReactionBoxes=true`. 4. Horizontal lines are not drawn when `InpH6DrawNodeLines=false`. 5. Red, green, and purple counts correspond to 20, 50, and 100 candles of post-confirmation survival without zone-end retouch. 6. Increasing `InpH6ReactionAwayBufferPoints` reduces confirmed reaction count. 7. Increasing `InpH6ReactionZoneEndBufferPoints` makes the invalidation stricter and ma

## Headings

- VAL0022 — H6 Reaction Box Zones
-   Release 141 zone projection test

## Entities

`M0001`, `VAL0022`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[docs/debug/H6_BOX_ALGORITHM_README|H6 Fast Box Visualizer — Official Algorithm]] — `debug_docs`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
