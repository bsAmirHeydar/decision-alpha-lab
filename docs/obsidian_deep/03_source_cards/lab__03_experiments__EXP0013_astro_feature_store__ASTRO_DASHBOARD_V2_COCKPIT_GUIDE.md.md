
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md"
source_ext: ".md"
source_size: 2704
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Execution / Risk", "MQL Native", "Path Smoothness", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]]

## Summary

This version replaces the crowded single oscillator cloud with a cockpit layout. The EA is research-only: no orders no iCustom no indicator path dependency no xlsx reading in MQL reads only runtime CSV draws text/cards directly with chart objects The dashboard does not delete and recreate all objects on every refresh. It updates the existing objects in-place. This avoids: flicker cut/return effect unstable live rendering overlapping text from stale labels Default professional layout: header/status card Path Quality card Micro M1 card Regime Engine card Macro Background card Prioritizes the smallest meaningful layer: Micro M1 Path Quality Regime Raw Axes Uses the older single preset text panel + row sparkline board. The header gives a fast verdict: This is not a trade signal. It is a path-quality diagnosis. Main market translation: CleanPath CleanImpulse BreakoutFT PullbackRisk ChopRisk M

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Dashboard V2 - Cockpit Layout
  - Main EA
  - Why the display is more stable
  - View modes
    - ASTRO_VIEW_COCKPIT
    - ASTRO_VIEW_MICRO_FOCUS
    - ASTRO_VIEW_SINGLE_PRESET
  - Recommended live inputs
  - Recommended historical/tester inputs
  - Reading order
    - 1) Header verdict
    - 2) Path Quality

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE|ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE|ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_EA_GUIDE|ASTRO_UNIFIED_DASHBOARD_EA_GUIDE.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
