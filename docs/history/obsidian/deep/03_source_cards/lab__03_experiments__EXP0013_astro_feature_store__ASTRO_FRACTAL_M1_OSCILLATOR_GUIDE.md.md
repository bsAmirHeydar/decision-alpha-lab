
---
type: source_card
source_path: "docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md"
source_ext: ".md"
source_size: 5875
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "MQL Native", "Path Smoothness", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md

## Source

[[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]]

## Summary

This guide documents the detailed fractal oscillator layer for EXP0013. The goal is to observe the **quality of one-minute movement** without turning the chart into a text wall. The indicator is research-only. It does not trade, does not predict direction, and does not modify orders. `EXP0013_AstroFractalOscillator` is the new detailed one. The CSV can be placed in either location: The reader also tries MetaQuotes Common Files as a fallback: Recommended input: The CSV already contains `broker_time`, so the indicator matches chart candle open time directly against CSV `broker_time`. There is no second GMT shift. The indicator has several display presets. Each preset uses the same data but plots a different logical layer. Shows the original Level 1 axes: Use this when you want the simplest raw read. Shows slow/background state: Meaning: `MacroFlow`: broad smoothness from slower geometry. `

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Fractal M1 Oscillator Guide
  - Indicator files
  - Runtime file rule
  - Presets
    - 1. RAW AXES
    - 2. MACRO BACKGROUND
    - 3. REGIME ENGINE
    - 4. MOON / MICRO M1
    - 5. M1 PATH QUALITY
    - 6. COMPACT JACKPOT
  - Fast reading models
    - Clean breakout window

## Related Source Documents

- [[mql5/Experts/AstroExecution/README|README.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `18`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE|ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md]] — score `18`
- [[docs/evidence/astro_professionalization_gap_map/b3f4b0da7c2e_ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `18`
- [[docs/evidence/exp0013_pure_astro_signal_algorithms/7e6eca7a86f8_ASTRO_PURE_SIGNAL_ALGORITHMS|ASTRO_PURE_SIGNAL_ALGORITHMS.md]] — score `18`
- [[docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE|ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
