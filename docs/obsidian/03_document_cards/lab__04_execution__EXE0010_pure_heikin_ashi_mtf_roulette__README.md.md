---
title: "EXE0010 — Pure Heikin Ashi MTF Roulette"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README.md"
source_ext: ".md"
category: "execution"
source_size_bytes: "3462"
entities:
  - "E0010"
  - "EXE0010"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# EXE0010 — Pure Heikin Ashi MTF Roulette

**Source:** [[lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README|lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README.md]]

**Category:** `execution`  
**Status:** ok  
**Size:** `3462` bytes

## خلاصه

E0010 is a pure Heikin Ashi execution module. It does not use structural nodes, M-regime labels, or continuation/reversal classifiers. It trades only from: current-forming higher-timeframe Heikin Ashi close/open body direction; completed lower-timeframe Heikin Ashi close/open body direction flip; Roulette risk sizing. Default: The M10 candle is intentionally the **current-forming** Heikin Ashi candle. The M1 trigger is intentionally based only on **closed** candles. The EA does not evaluate entry logic on every tick. It runs the execution decision only once when a new lower-timeframe bar opens. This means the previous M1 candle has just closed, and only that completed candle is allowed to tr

## Headings

- EXE0010 — Pure Heikin Ashi MTF Roulette
-   Purpose
-   Timeframes
-   Execution clock
-   Heikin Ashi body direction
-   Buy rule
-   Sell rule
-   Risk and target
-   Corrected Roulette logic
-   Files

## Entities

`E0010`, `EXE0010`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
