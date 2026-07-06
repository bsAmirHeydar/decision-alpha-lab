---
title: "E0006 — Revisit-Only Entry Logic"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/E0006/REVISIT_ONLY_README.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "3889"
entities:
  - "E0006"
  - "M0001"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0006 — Revisit-Only Entry Logic

**Source:** [[docs/debug/E0006/REVISIT_ONLY_README|docs/debug/E0006/REVISIT_ONLY_README.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `3889` bytes

## خلاصه

The revisit-only mode is designed for experiments where the first touch of a zone is not traded. The zone must first survive a non-hunted touch cycle, then become tradeable only on a later revisit, and only if both the first cycle and the revisit cycle satisfy the internal hunt standard. When `InpOnlyTradeRevisitZones=false`, E0006 behaves like the standard entry-qualification mode. When `InpOnlyTradeRevisitZones=true`, first-touch entries are skipped and the origin must prove a prior non-hunted touch event. `InpRevisitMinInternalHunts=0` means reuse the standard threshold: A revisit-only trade requires this lifecycle: For a LOW origin: The logic is: For a HIGH origin: The logic is: The firs

## Headings

- E0006 — Revisit-Only Entry Logic
-   Inputs
-   Required sequence
-   LOW origin / BUY revisit
-   HIGH origin / SELL revisit
-   Why the first cycle must qualify
-   What counts as a prior touch
-   Important implication
-   Recommended test setup

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
