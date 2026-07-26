---
title: "E0006 — Entry Qualification Logic"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/E0006/ENTRY_QUALIFICATION_README.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "3944"
entities:
  - "E0006"
  - "M0001"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0006 — Entry Qualification Logic

**Source:** [[docs/debug/E0006/ENTRY_QUALIFICATION_README|docs/debug/E0006/ENTRY_QUALIFICATION_README.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `3944` bytes

## خلاصه

This document describes how E0006 decides whether a structural zone is allowed to receive a limit order. The entry decision is not simply “every zone gets an order.” The current executor can require the path after the origin node to prove that enough same-side internal nodes were hunted before the origin zone becomes tradeable. E0006 uses two L values. The origin node is the anchor of the trade. The internal nodes are the evidence that price has created and hunted enough same-side liquidity before the order is allowed. Inputs: With this setup, a zone is not eligible until at least three same-side internal nodes have been hunted after the origin node. For a LOW origin, E0006 is considering a

## Headings

- E0006 — Entry Qualification Logic
-   Origin versus internal nodes
-   Standard same-side hunt filter
-   LOW origin / BUY logic
-   HIGH origin / SELL logic
-   Hunt definition
-   Decision window
-   Same-side toggle
-   Interaction with pending caps
-   Fast test settings

## Entities

`E0006`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
