
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml"
source_ext: ".yaml"
source_size: 511
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "Known-Time Causality", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0013", "H0009"]
---

# Source Card — metadata.yaml

## Source

[lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml](../../lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml)

## Summary

id: EXP0013 name: Astro Feature Store hypothesis: H0009 status: draft language: runtime: MQL5 feature_builder: Python purpose: Candle-aligned astrological feature store for Distribution Engineering. causality: timestamp_basis: broker candle open time utc_conversion: utc_time = broker_time - broker_gmt_offset_hours no_future_market_data: true execution_effect: none outputs: Python-generated astro CSV MQL5 feature row lookup MQL5 visual tester panel distribution feature key adapter

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013, H0009

## Headings

- —

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|BUILD_EXCEL_COMMANDS.md]] — score `18`
- [[docs/research/H0009_astro_feature_store_distribution_engineering|H0009_astro_feature_store_distribution_engineering.md]] — score `17`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_FIX|ASTRO_CSV_RUNTIME_PATH_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO_DOCTRINE_V1.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
