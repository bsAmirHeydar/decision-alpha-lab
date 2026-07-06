
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT.md"
source_ext: ".md"
source_size: 3167
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Convexity / Optionality", "Execution / Risk", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_ONLY_EXECUTION_CONTRACT.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT.md]]

## Summary

This document defines the purity rules for turning EXP0013 from an astro data store into an astro-only execution program. Allowed inputs: transit planetary state natal or inception chart state transit-to-transit aspects transit-to-natal aspects houses, angles, and angularity declination, parallels, contra-parallels dignity, element, modality, retrograde, station, ingress moon phase and illumination Forbidden inputs: price structure ATR market session filters volume indicator outputs support/resistance from market data any market-derived target/stop logic inside the pure astro signal engine The pure astro layer must be explainable entirely in astrological language. Every row must be knowable at candle open. `broker_time` is the lookup key in MQL5. `utc_time` is already stored by Python. MQL5 must not apply a second time shift. Applying/separating must be derived from instantaneous planeta

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0013

## Headings

- EXP0013 Astro-Only Execution Contract
  - 1. Purity contract
  - 2. Time contract
  - 3. Natal contract
  - 4. Doctrine contract
  - 5. Feature contract
  - 6. Entry contract
  - 7. Exit contract
  - 8. Validation contract
  - 9. Logging contract
  - 10. Production contract

## Related Source Documents

- [metadata.yaml](../../lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml) — score `24`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `22`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `22`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `21`
- [[tools/astro_live_bridge/README|README.md]] — score `21`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PURE_SIGNAL_ALGORITHMS|ASTRO_PURE_SIGNAL_ALGORITHMS.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_RADICAL_REDESIGN|ASTRO_RAW_SKY_RADICAL_REDESIGN.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
