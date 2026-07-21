---
title: "H6 Reaction Box Zones"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/H6_REACTION_BOX_ZONES.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "14450"
entities:
  - "M0001"
  - "M0002"
  - "M0006"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# H6 Reaction Box Zones

**Source:** [[docs/debug/H6_REACTION_BOX_ZONES|docs/debug/H6_REACTION_BOX_ZONES.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `14450` bytes

## خلاصه

Release 112 changes the official H6 chart visual from simple horizontal survivor lines to reaction-zone rectangles. Contract: Raw M0001 nodes only. No M0002 branch samples. Same-known-time events are never internally ordered. A reaction box starts from the known node time and ends at the first future touch. The vertical box spans from the node price to the touch extreme. For a high node, the touch extreme is the touch candle high; the expected reaction is downward. For a low node, the touch extreme is the touch candle low; the expected reaction is upward. After touch, reversal confirmation must happen on a later candle. This avoids hidden OHLC sequence assumptions inside the touch candle. On

## Headings

- H6 Reaction Box Zones
-   Release 141 — node-capped projection

## Entities

`M0001`, `M0002`, `M0006`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[README|Decision Alpha Lab]] — `readme`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/03_validation/VAL0013_h4_fast_atomic_extended/README|VAL0013 — H4 Fast Atomic Extended Diagnostics]] — `validation`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
