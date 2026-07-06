---
title: "EXP0012 — Distributional Cluster Miner"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0012_distributional_cluster_miner/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "4872"
entities:
  - "E0011"
  - "EXP0012"
concepts:
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
---


# EXP0012 — Distributional Cluster Miner

**Source:** [[lab/03_experiments/EXP0012_distributional_cluster_miner/README|lab/03_experiments/EXP0012_distributional_cluster_miner/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `4872` bytes

## خلاصه

**Distribution Engineering for Conditional Sequence Extraction** This experiment turns each execution system into a distribution generator. The goal is not only to measure whether an execution has an edge. The goal is to identify the causal feature states where wins become clustered and therefore suitable for Roulette / Jackpot execution. The central shift is: A raw strategy may have mediocre global statistics while still containing a narrow feature regime where the conditional probability of a next win after a win is much higher than the raw win rate. That is the object we want to mine. The module is MQL5-only and research-only. It never sends orders. For every feature group, the miner calc

## Headings

- EXP0012 — Distributional Cluster Miner
-   Title
-   Module Files
-   What the module measures
-   Core metrics
-     Raw win rate
-     Filtered win rate
-     Lift
-     Conditional win-after-win
-     Cluster counts
-   Integration contract for execution modules
-   Design principle

## Entities

`E0011`, `EXP0012`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/04_execution/EXE0011_donchian20_atr3_roulette/README|EXE0011 — Donchian 20 ATR3 Roulette Execution]] — `execution`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
