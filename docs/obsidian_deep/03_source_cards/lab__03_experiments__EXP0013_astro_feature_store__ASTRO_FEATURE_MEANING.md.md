
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING.md"
source_ext: ".md"
source_size: 5726
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Execution / Risk", "Known-Time Causality", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_FEATURE_MEANING.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING.md]]

## Summary

This document defines what each astrological raw field can become as a testable feature. The project does not assume that astrology is causal. In Decision Alpha Lab, astrology is treated as a high-dimensional **time-state feature map**. A feature is useful only if it produces measurable distributional lift,… Raw columns: Derived features: Meaning: Longitude is the cyclic angular location of a body on the ecliptic. For research, it tells us where the body is inside its 360-degree cycle. We do not trade the longitude itself; we test whether market outcomes are distr… Example feature key: Raw columns: Derived features: Meaning: Latitude measures distance north/south of the ecliptic. In research, this is a secondary geometry feature. It can be tested for path, volatility, and breakout distribution changes, but it should not be over-weighted unti… Raw columns: Derived features: Meaning: Dista

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXP0013

## Headings

- EXP0013 — Astro Feature Meaning and Research Semantics
  - 1. Longitude
  - 2. Latitude
  - 3. Distance
  - 4. Longitude Speed
  - 5. Declination
  - 6. Moon Phase
  - 7. Aspects
  - 8. Feature hierarchy
    - Full raw key
    - Research key
    - Compact execution key

## Related Source Documents

- [[docs/research/H0009_astro_feature_taxonomy|H0009_astro_feature_taxonomy.md]] — score `21`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_RADICAL_REDESIGN|ASTRO_RAW_SKY_RADICAL_REDESIGN.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|BUILD_EXCEL_COMMANDS.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
