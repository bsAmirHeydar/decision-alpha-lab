
---
type: source_card
source_path: "mql5/Experts/AstroExecution/README.md"
source_ext: ".md"
source_size: 5603
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Convexity / Optionality", "Execution / Risk", "Licensing", "MQL Native", "Path Smoothness", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXP0013"]
---

# Source Card — README.md

## Source

[[mql5/Experts/AstroExecution/README|mql5/Experts/AstroExecution/README.md]]

## Summary

This folder contains astro-only Expert Advisors for EXP0013. They read the deterministic astro CSV through `DAL_AstroExcelCandleReader.mqh`. They use `DAL_AstroPureAstrologySignals.mqh`. They can journal paper actions through `DAL_AstroExecutionJournal.mqh`. They do not use market-structure, indicators, ATR, volume, or execution-family context. They emit pure astrology entry and exit language from transit, natal activation, and doctrinal astro metrics. They now read a hierarchical timing stack: macro field -> meso gate -> micro trigger -> minute window. They can load doctrine-owned threshold defaults from `DAL_AstroFamilyThresholds.mqh`. The pure signal layer now includes sect-aware doctrine context plus benefic / malefic and house lift / drag scores. The raw map now also exposes explicit dignity, dispositor, reception/chain, station-intensity, ingress-intensity, solar-quarter, and eclip

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0013

## Headings

- Astro Execution
  - Contract
  - Execution families
    - A0001 - Transit Trend Pulse
    - A0002 - Natal Resonance
    - A0003 - Friction Polarity
    - A0004 - Sect Benefic Pressure
    - A0005 - Moon Timing Window
    - A0006 - Angular Activation
    - A0007 - Station Transition
    - A0090 - Live Order Shell
  - Usage

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `21`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE|ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PURE_SIGNAL_ALGORITHMS|ASTRO_PURE_SIGNAL_ALGORITHMS.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|BUILD_EXCEL_COMMANDS.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/RUN_ASTRO_RAW_AXES_OSCILLATOR|RUN_ASTRO_RAW_AXES_OSCILLATOR.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
