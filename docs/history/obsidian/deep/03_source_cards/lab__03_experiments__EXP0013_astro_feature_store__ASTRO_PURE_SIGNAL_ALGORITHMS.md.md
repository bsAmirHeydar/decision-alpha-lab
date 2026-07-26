
---
type: source_card
source_path: "docs/evidence/exp0013_pure_astro_signal_algorithms/7e6eca7a86f8_ASTRO_PURE_SIGNAL_ALGORITHMS.md"
source_ext: ".md"
source_size: 8513
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Decision Node", "Execution / Risk", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_PURE_SIGNAL_ALGORITHMS.md

## Source

[[docs/evidence/exp0013_pure_astro_signal_algorithms/7e6eca7a86f8_ASTRO_PURE_SIGNAL_ALGORITHMS|docs/evidence/exp0013_pure_astro_signal_algorithms/7e6eca7a86f8_ASTRO_PURE_SIGNAL_ALGORITHMS.md]]

## Summary

This document describes the current pure astro signal layer introduced for the first astro-only execution families. This layer is intentionally narrow: no market features no price structure no ATR no volatility from price Everything below is derived from the astro row plus the existing astro path and fractal metrics. The signal layer reads: raw body state from `DAL_AstroMapRow` raw aspect state from `DAL_AstroMapRow` natal activation state when present path/fractal metrics from `DAL_AstroFractalPathMetrics.mqh` canonical astro language fields from the CSV row `DAL_AstroPureSignal` produces: `long_bias_score` `short_bias_score` `trend_score` `path_score` `friction_score` `volatility_score` `natal_activation_score` `entry_score` `exit_score` `regime_name` `direction_name` `entry_signal` `exit_signal` `astro_language` `astro_trade_key` `sect_name` `benefic_support_score` `malefic_pressure_s

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0013

## Headings

- EXP0013 Pure Astro Signal Algorithms
  - Scope
  - Inputs
  - Core outputs
  - Long bias
  - Short bias
  - Trend score
  - Path score
  - Friction score
  - Volatility score
  - Natal activation score
  - Sect-aware doctrine

## Related Source Documents

- [[docs/evidence/astro_professionalization_gap_map/b3f4b0da7c2e_ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `22`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO_DOCTRINE_V1.md]] — score `20`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `20`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `20`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `19`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `18`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_EA_GUIDE|ASTRO_UNIFIED_DASHBOARD_EA_GUIDE.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
