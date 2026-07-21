---
title: "Astro Feature Builder"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "tools/astro_feature_builder/README.md"
source_ext: ".md"
category: "tool_docs"
source_size_bytes: "3958"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
---


# Astro Feature Builder

**Source:** [[tools/astro_feature_builder/README|tools/astro_feature_builder/README.md]]

**Category:** `tool_docs`  
**Status:** ok  
**Size:** `3958` bytes

## خلاصه

Python-side deterministic generator for candle-aligned astrological feature stores. Primary runtime architecture: The builder uses `pyswisseph` / Swiss Ephemeris. It does not call APIs and does not require internet during generation once dependencies and ephemeris files are available. Every row is computed at candle open time. This keeps the data causal for Strategy Tester and live execution. The builder can optionally embed a fixed natal or inception chart into every row: When natal inputs are present, the CSV also contains: natal body positions and houses natal ASC / MC / cusps transit-to-natal aspects for Sun..Saturn transit-to-transit and transit-to-natal declination parallels / contra-p

## Headings

- Astro Feature Builder
-   Install
-   Generate CSV + Excel
-   Time contract
-   Natal / inception support
-   Doctrine metadata
-   JSON config
-   MQL5 runtime
-   Excel limit

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README|EXE0010 — Pure Heikin Ashi MTF Roulette]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
