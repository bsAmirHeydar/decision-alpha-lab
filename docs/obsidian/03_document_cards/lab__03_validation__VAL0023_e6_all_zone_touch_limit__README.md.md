---
title: "E0006 — All-Zone Touch Limit Fixed-R Executor"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0023_e6_all_zone_touch_limit/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "9394"
entities:
  - "E0006"
  - "M0001"
concepts:
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# E0006 — All-Zone Touch Limit Fixed-R Executor

**Source:** [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|lab/03_validation/VAL0023_e6_all_zone_touch_limit/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `9394` bytes

## خلاصه

E0006 is a lightweight execution module that uses existing M0001 / execution modules instead of rebuilding structure logic. Source of truth for zones: M0001 live territory logic. Scan all confirmed structural nodes by default. No maximum trade-count cap by default. One managed pending limit order per live, non-hunted M0001 zone. New-bar only execution. No tick-by-tick recalculation. Stop loss is the far end of the zone. Take profit is fixed-R, default `20R`. LOW node / support zone: HIGH node / resistance zone: The sell-side SL and TP spread shift follows the requested execution rule. `InpMaxNodesScan=0` means all confirmed nodes are scanned. This is not a trade limit. The EA upserts each ma

## Headings

- E0006 — All-Zone Touch Limit Fixed-R Executor
-   Contract
-   Direction
-   Important inputs
-   Order lifecycle
-   Compile target
-   Release 101 — per-side pending-order caps
-   Release 102 — open-position side blocking
-   Documentation added in Release 108
-   Release 109 modular kernel
-   Release 110 revisit secondary-node anchors

## Entities

`E0006`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/E0006/MODULE_KERNEL_README|E0006 Modular Execution Kernel]] — `debug_docs`
- [[docs/debug/E0006/ENTRY_QUALIFICATION_README|E0006 — Entry Qualification Logic]] — `debug_docs`
- [[docs/debug/E0006/EXIT_AND_RISK_README|E0006 — Exit, Stop, Spread, and Risk Logic]] — `debug_docs`
- [[docs/debug/E0006/INPUT_REFERENCE_README|E0006 — Input Reference]] — `debug_docs`
- [[docs/debug/E0006/REVISIT_ONLY_README|E0006 — Revisit-Only Entry Logic]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
