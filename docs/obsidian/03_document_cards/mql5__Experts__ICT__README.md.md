---
title: "ICT Experts"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "mql5/Experts/ICT/README.md"
source_ext: ".md"
category: "mql5_docs"
source_size_bytes: "296"
entities:
  - "EXP0014"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
---


# ICT Experts

**Source:** [[mql5/Experts/ICT/README|mql5/Experts/ICT/README.md]]

**Category:** `mql5_docs`  
**Status:** short  
**Size:** `296` bytes

## خلاصه

Batch expert for EXP0014 ICT: L-node sweep -> FVG in sweep path -> IFVG -> CISD -> RR filter -> CSV journal. The expert is intentionally not tick-driven. `OnTick()` is empty. By default it runs once on init, writes CSV files, and removes itself.

## Headings

- ICT Experts
-   ICT001_SweepIFVGCISDExecutor

## Entities

`EXP0014`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0012_distributional_cluster_miner/README|EXP0012 — Distributional Cluster Miner]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|EXP0015 Intermarket Candle + Session Divergence]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
