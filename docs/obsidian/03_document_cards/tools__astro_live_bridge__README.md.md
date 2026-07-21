---
title: "EXP0013 Astro Live Bridge V2"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "tools/astro_live_bridge/README.md"
source_ext: ".md"
category: "tool_docs"
source_size_bytes: "2891"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Convexity"
  - "Execution"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
---


# EXP0013 Astro Live Bridge V2

**Source:** [[tools/astro_live_bridge/README|tools/astro_live_bridge/README.md]]

**Category:** `tool_docs`  
**Status:** ok  
**Size:** `2891` bytes

## خلاصه

This bridge generates a small rolling astro CSV for the live MT5 dashboard. Python writes: `broker_time`: already aligned to the broker chart time `utc_time`: true UTC used for astronomical calculations MQL5 reads `broker_time` directly. There is no second GMT shift inside MQL. Written atomically into Common Files: The status JSON is for human/live diagnostics and includes: last update UTC output CSV path broker start/end window rows hint error text if generation failed The live bridge can pass house-location inputs to the builder: If `--house-lat` and `--house-lon` are omitted, the CSV remains geocentric-only and the MQL dashboard will show houses as unavailable. The live bridge can also bu

## Headings

- EXP0013 Astro Live Bridge V2
-   Runtime contract
-   One-shot test
-   Continuous live mode
-   MT5 EA inputs
-   Output files
-   Optional house cusps
-   Optional natal or inception chart

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[mql5/Experts/AstroExecution/README|Astro Execution]] — `mql5_docs`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/finalization/README|EXP0013 Finalization Snapshot]] — `experiment`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README|EXE0010 — Pure Heikin Ashi MTF Roulette]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
