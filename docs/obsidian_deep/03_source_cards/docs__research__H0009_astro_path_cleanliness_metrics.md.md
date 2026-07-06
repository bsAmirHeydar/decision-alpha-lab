
---
type: source_card
source_path: "docs/research/H0009_astro_path_cleanliness_metrics.md"
source_ext: ".md"
source_size: 1049
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "Known-Time Causality", "Path Smoothness"]
entities: ["H0009"]
---

# Source Card — H0009_astro_path_cleanliness_metrics.md

## Source

[[docs/research/H0009_astro_path_cleanliness_metrics|docs/research/H0009_astro_path_cleanliness_metrics.md]]

## Summary

This note defines the first Decision Alpha Lab interpretation layer for astrological data. The project does not use astrology as a raw directional signal. It uses astrological states as causal time features for Distribution Engineering. The first target is path cleanliness: lower adverse excursion, shallower p… The interpretation layer converts raw ephemeris data into seven axes: Flow Impulse Friction Pressure Transition Moon Tempo Saturn Drag It then derives composite scores: Clean Path Clean Impulse Smooth Continuation Breakout Follow-through Pullback Risk Chop Risk These scores are not trading signals. They are feature candidates. Their value must be validated by attaching them to execution outcomes and measuring MAE_R, MFE_R, pullback_depth_R, path_efficiency, clean target hit rat…

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]]

## Entities

H0009

## Headings

- H0009 — Astro Path Cleanliness Metrics

## Related Source Documents

- [[docs/research/H0009_astro_feature_store_distribution_engineering|H0009_astro_feature_store_distribution_engineering.md]] — score `12`
- [metadata.yaml](../../lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml) — score `11`
- [signals.yaml](../../registry/signals.yaml) — score `10`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|README.md]] — score `8`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_MARKET_ANATOMY_PHILOSOPHY|README_FLAG_MARKET_ANATOMY_PHILOSOPHY.md]] — score `8`
- [[tools/astro_ml/README|README.md]] — score `8`
- [[lab/07_monitoring/MON001/metrics|metrics.md]] — score `8`
- [[docs/research/H0009_astro_feature_taxonomy|H0009_astro_feature_taxonomy.md]] — score `7`
- [[docs/architecture|architecture.md]] — score `6`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
