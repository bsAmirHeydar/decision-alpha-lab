---
title: "VAL0025 — E0008 MTF Purple Extreme Validation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0025_e8_mtf_purple_extreme/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "1682"
entities:
  - "E0008"
  - "VAL0025"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# VAL0025 — E0008 MTF Purple Extreme Validation

**Source:** [[lab/03_validation/VAL0025_e8_mtf_purple_extreme/README|lab/03_validation/VAL0025_e8_mtf_purple_extreme/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `1682` bytes

## خلاصه

Find whether multi-timeframe context can filter purple/source zones into tiny-stop high-R candidates. A good candidate should show: Do not judge this by number of trades. The desired outcome is a small number of very asymmetric plans. Recommended first run: The EA should now rebuild: H1/H4/M15 context only when those timeframes print a new candle. Execution map only once per M1 candle. Nothing structural on every tick.

## Headings

- VAL0025 — E0008 MTF Purple Extreme Validation
-   Goal
-   Main settings
-   Test matrix
-     A. No-future mode
-     B. Oracle purple mode
-     C. Micro tiny-stop mode
-   What to inspect in the log
-   Important
-   Release 101 performance settings

## Entities

`E0008`, `VAL0025`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[lab/03_validation/VAL0006_h5_live_touch_replay/README|VAL0006 — H5 live-valid touch-entry replay]] — `validation`
- [[lab/03_validation/VAL0007_h5_causal_live_replay/README|VAL0007 — H5 Causal Live Replay]] — `validation`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[lab/03_validation/VAL0024_e7_purple_source_extreme/README|VAL0024 — E0007 Purple Source Extreme Execution Validation]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
