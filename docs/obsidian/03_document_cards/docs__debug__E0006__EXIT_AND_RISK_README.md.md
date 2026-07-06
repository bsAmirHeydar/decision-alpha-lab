---
title: "E0006 — Exit, Stop, Spread, and Risk Logic"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/E0006/EXIT_AND_RISK_README.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "5995"
entities:
  - "E0006"
  - "M0001"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0006 — Exit, Stop, Spread, and Risk Logic

**Source:** [[docs/debug/E0006/EXIT_AND_RISK_README|docs/debug/E0006/EXIT_AND_RISK_README.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `5995` bytes

## خلاصه

This document explains how E0006 places entries, anchors stops, handles spread, sizes risk, and manages take profit after a trade opens. E0006 uses limit orders on structural zones. For LOW origin zones: The BUY entry is shifted upward because a buy fills on Ask. This adjustment is intentionally preserved even when stop mode changes. For HIGH origin zones: The SELL entry remains at the lower edge of the high/supply zone. Inputs: E0006 now has two revisit entry anchors and three stop anchors. Origin-zone revisit entry: This keeps the order on the original M0001 zone when the node revisits. Secondary-node revisit entry: This is only meaningful when `InpOnlyTradeRevisitZones = true`. After the

## Headings

- E0006 — Exit, Stop, Spread, and Risk Logic
-   Entry prices
-   Stop anchor modes
-     Revisit entry anchors
-     Stop anchor 1: origin zone back
-     Stop anchor 2: origin node
-     Stop anchor 3: revisit secondary node
-   Risk distance
-   Fixed-R TP
-   Internal opposite-node TP manager
-     BUY position exit
-     SELL position exit

## Entities

`E0006`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
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
