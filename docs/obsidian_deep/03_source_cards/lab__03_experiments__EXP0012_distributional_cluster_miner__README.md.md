
---
type: source_card
source_path: "lab/03_experiments/EXP0012_distributional_cluster_miner/README.md"
source_ext: ".md"
source_size: 4872
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Known-Time Causality", "MQL Native", "UI / React"]
entities: ["E0011", "EXP0012"]
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP0012_distributional_cluster_miner/README|lab/03_experiments/EXP0012_distributional_cluster_miner/README.md]]

## Summary

**Distribution Engineering for Conditional Sequence Extraction** This experiment turns each execution system into a distribution generator. The goal is not only to measure whether an execution has an edge. The goal is to identify the causal feature states where wins become clustered a… The central shift is: A raw strategy may have mediocre global statistics while still containing a narrow feature regime where the conditional probability of a next win after a win is much higher than the raw win rate. That is the object we want to mine. The module is MQL5-only and research-only. It never sends orders. For every feature group, the miner calculates: Global probability of a win in the unfiltered trade population. Win probability inside one causal feature group. How much the feature group improves win probability versus the raw distribution. The key Roulette / Jackpot metric. A filter is not v

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

E0011, EXP0012

## Headings

- EXP0012 — Distributional Cluster Miner
  - Title
  - Module Files
  - What the module measures
  - Core metrics
    - Raw win rate
    - Filtered win rate
    - Lift
    - Conditional win-after-win
    - Cluster counts
  - Integration contract for execution modules
  - Design principle

## Related Source Documents

- [[docs/research/H0009_astro_feature_store_distribution_engineering|H0009_astro_feature_store_distribution_engineering.md]] — score `15`
- [[lab/04_execution/EXE0011_donchian20_atr3_roulette/README|README.md]] — score `13`
- [[docs/articles/distribution_engineering_for_conditional_sequence_extraction|distribution_engineering_for_conditional_sequence_extraction.md]] — score `11`
- [metadata.yaml](../../lab/03_experiments/EXP0012_distributional_cluster_miner/metadata.yaml) — score `10`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `10`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|BUILD_EXCEL_COMMANDS.md]] — score `10`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|README.md]] — score `10`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_MARKET_ANATOMY_PHILOSOPHY|README_FLAG_MARKET_ANATOMY_PHILOSOPHY.md]] — score `10`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `10`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
