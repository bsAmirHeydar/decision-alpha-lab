
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/README.md"
source_ext: ".md"
source_size: 6016
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Execution / Risk", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXP0013"]
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/README|lab/03_experiments/EXP0013_astro_feature_store/README.md]]

## Summary

EXP0013 is the deterministic astronomy-to-MQL pipeline inside Decision Alpha Lab. It now supports both: transit-only raw sky state natal or inception chart activation models The goal is to make every candle in tester or live execution able to read a full astro state row without calling Python or external APIs at runtime. transit raw bodies transit houses and angles transit-to-transit aspects transit declination speed and out-of-bounds state transit-to-transit parallels and contra-parallels natal raw bodies natal houses and angles transit-to-natal aspects for Sun..Saturn transit-to-natal parallels and contra-parallels for Sun..Saturn transit placement inside natal houses pure astro language fields doctrine and schema metadata embedded into every row Python computes astro rows at candle open time. CSV stores both `broker_time` and `utc_time`. MQL looks up by `broker_time` exactly. MQL does

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0013

## Headings

- EXP0013 - Astro Feature Store
  - Purpose
  - Main architecture
  - Current modules
  - Data families now supported
  - Build a transit + natal CSV
  - Runtime contract
  - Dashboard
  - Astro-only execution
  - Research discipline
  - Important note

## Related Source Documents

- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `30`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `28`
- [[docs/evidence/exp0013_pure_astro_signal_algorithms/7e6eca7a86f8_ASTRO_PURE_SIGNAL_ALGORITHMS|ASTRO_PURE_SIGNAL_ALGORITHMS.md]] — score `28`
- [[docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `28`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO_DOCTRINE_V1.md]] — score `26`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|ASTRO_FEATURE_MEANING.md]] — score `26`
- [metadata.yaml](../../lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml) — score `24`
- [[docs/architecture|architecture.md]] — score `22`
- [[docs/evidence/astro_professionalization_gap_map/b3f4b0da7c2e_ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `20`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
