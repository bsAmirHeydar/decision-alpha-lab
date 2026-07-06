---
title: "E0006 Modular Execution Kernel"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/E0006/MODULE_KERNEL_README.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "6061"
entities:
  - "E0006"
  - "M0001"
concepts:
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0006 Modular Execution Kernel

**Source:** [[docs/debug/E0006/MODULE_KERNEL_README|docs/debug/E0006/MODULE_KERNEL_README.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `6061` bytes

## خلاصه

This document describes the reusable modules extracted from the E0006 execution work. The goal is to stop rewriting the same structural ideas inside every EA and instead compose them from small, testable pieces. E0006 accumulated several independent ideas: 1. origin zones from M0001 structural nodes, 2. internal same-side hunt qualification, 3. optional revisit-only entries, 4. node-price versus zone-back stop anchoring, 5. pending-order and open-position side caps, 6. zero initial fixed-R TP with an internal opposite-node TP manager, 7. strict new-candle synchronization instead of tick-heavy computation. Each idea is useful alone. A future executor may want only the internal-hunt filter, on

## Headings

- E0006 Modular Execution Kernel
-   Why this layer exists
-   Files
-   1. Types and policies
-   2. Internal hunt qualification
-   3. Zone pricing and stop anchoring
-   4. Revisit-only cycle qualification
-   5. Internal opposite-node TP
-   6. Exposure caps
-   Suggested future migration
-   Design rule

## Entities

`E0006`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
