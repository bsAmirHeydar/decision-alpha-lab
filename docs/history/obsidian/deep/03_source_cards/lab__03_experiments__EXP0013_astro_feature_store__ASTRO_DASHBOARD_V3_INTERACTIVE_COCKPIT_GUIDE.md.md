
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md"
source_ext: ".md"
source_size: 3144
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "MQL Native", "Path Smoothness", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]]

## Summary

This patch upgrades the dashboard into a more professional interactive cockpit. cleaner screen layout all major astro states visible open/close behavior through clickable chart buttons cockpit mode and focus mode more useful diagnostics when the row is not found stable redraws without tick-by-tick flicker The dashboard now has clickable chart buttons: `COCKPIT` `PATH` `MICRO` `REGIME` `MACRO` `RAW` `TEXT ON/OFF` `OSC ON/OFF` section toggles: `PTH` `MIC` `REG` `MAC` `RAW` `RELOAD` Shows multiple cards at once: Path Quality Micro M1 Regime Engine Macro Background Raw Axes Diagnostics Shows one selected section in larger form, plus diagnostics and oscillator. In cockpit mode you can hide or show each section using the short toggle buttons: `PTH` `MIC` `REG` `MAC` `RAW` This gives the requested open/close workflow without relying on a separate custom indicator. When the chart says `ROW NOT F

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Dashboard V3 - Interactive Cockpit
  - Main goals
  - File
  - What changed
    - 1) Interactive header controls
    - 2) Two view modes
      - Cockpit mode
      - Focus mode
    - 3) Open/close behavior
    - 4) Better diagnostics
  - Live usage recommendation
  - Historical usage recommendation

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE|ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE|ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_EA_GUIDE|ASTRO_UNIFIED_DASHBOARD_EA_GUIDE.md]] — score `18`
- [[docs/evidence/run_exp0013_astro_raw_axes_oscillator/1cf21803c17b_RUN_ASTRO_RAW_AXES_OSCILLATOR|RUN_ASTRO_RAW_AXES_OSCILLATOR.md]] — score `18`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `17`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
