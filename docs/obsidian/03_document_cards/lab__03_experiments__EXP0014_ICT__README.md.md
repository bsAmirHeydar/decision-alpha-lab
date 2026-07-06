---
title: "EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0014_ICT/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "3341"
entities:
  - "EXP0014"
concepts:
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab

**Source:** [[lab/03_experiments/EXP0014_ICT/README|lab/03_experiments/EXP0014_ICT/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `3341` bytes

## خلاصه

This experiment is a deterministic, bar-based ICT module scaffold for Decision Alpha Lab. It does **not** run on every tick. The default expert runs once on init, scans historical bars, writes CSV journals, and removes itself. Source: `mql5/Include/ICT/DAL_ICTSweepDetector.mqh` Uses the existing DAL structural node engine: `DAL_DetectConfirmedStructuralNodes` L-rule confirmed highs/lows active-from index/time is respected to avoid future leakage A high node sweep creates a bearish setup context. A low node sweep creates a bullish setup context. Modes: `ICT_SWEEP_TOUCH`: price reaches the configured node zone touch depth. `ICT_SWEEP_HUNT`: price pierces the node zone and closes back through t

## Headings

- EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab
-   Core modules
-     1. L-node sweep
-     2. FVG / IFVG
-     3. CISD
-     4. Execution model
-   Default expert
-   Output
-   Research warning

## Entities

`EXP0014`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/ICT/README|ICT Experts]] — `mql5_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README|EXE0010 — Pure Heikin Ashi MTF Roulette]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
