
---
type: source_card
source_path: "lab/03_experiments/EXP0012_distributional_cluster_miner/metadata.yaml"
source_ext: ".yaml"
source_size: 903
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native", "Python Brain"]
entities: ["EXP0012"]
---

# Source Card — metadata.yaml

## Source

[lab/03_experiments/EXP0012_distributional_cluster_miner/metadata.yaml](../../lab/03_experiments/EXP0012_distributional_cluster_miner/metadata.yaml)

## Summary

id: EXP0012 title: Distributional Cluster Miner hypothesis: H0008_distribution_engineering type: research_module language: MQL5 status: draft scope: distribution_engineering conditional_sequence_extraction cluster_mining roulette_permission_layer outputs: raw_distribution_metrics feature_group_metrics conditional_win_after_win_metrics cluster_counts eligibility_decisions csv_report mql5: include: mql5/Include/Research/DAL_DistributionEngineeringTypes.mqh mql5/Include/Research/DAL_DistributionClusterMiner.mqh mql5/Include/Research/DAL_DistributionClusterFilter.mqh mql5/Include/Research/DAL_DistributionExecutionAdapter.mqh demo_expert: mql5/Experts/Research/EXP0012_DistributionClusterMiner_Demo.mq5 notes: Research-only module. Does not send orders. Designed to be embedded in execution EAs after trade close.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

## Entities

EXP0012

## Headings

- —

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[docs/research/H0009_astro_feature_store_distribution_engineering|H0009_astro_feature_store_distribution_engineering.md]] — score `11`
- [[lab/03_experiments/EXP0012_distributional_cluster_miner/README|README.md]] — score `10`
- [[docs/research/H0008_distribution_engineering|H0008_distribution_engineering.md]] — score `10`
- [H0008_EXP0012_distribution_engineering.yaml](../../registry/patches/H0008_EXP0012_distribution_engineering.yaml) — score `9`
- [[lab/03_experiments/EXP0000_sample/report|report.md]] — score `8`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|report.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
