---
title: "VAL0021 — H6 Node Survival Map"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0021_h6_node_survival_map/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "714"
entities:
  - "VAL0021"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# VAL0021 — H6 Node Survival Map

**Source:** [[lab/03_validation/VAL0021_h6_node_survival_map/README|lab/03_validation/VAL0021_h6_node_survival_map/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `714` bytes

## خلاصه

Run `M0006_NodeSurvivalMap.mq5` on the target symbol/timeframe. Recommended daily settings: Validation checks: build sanity says `officialReport=H0006_NODE_SURVIVAL_MAP` audit says `sampleCalls=0`, `branchSamplesBuilt=0`, `m0002Calls=0` horizons are `20/50/100` chart update reports object counts and prefix `DAL_H6_NODE_` MetaTrader chart shows red, green, and purple horizontal node levels when enabled

## Headings

- VAL0021 — H6 Node Survival Map

## Entities

`VAL0021`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/03_validation/VAL0006_h5_live_touch_replay/README|VAL0006 — H5 live-valid touch-entry replay]] — `validation`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
