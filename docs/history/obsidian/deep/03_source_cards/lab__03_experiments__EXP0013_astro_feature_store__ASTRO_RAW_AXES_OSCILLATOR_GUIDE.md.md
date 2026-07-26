
---
type: source_card
source_path: "docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md"
source_ext: ".md"
source_size: 4526
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "MQL Native", "Path Smoothness", "Python Brain", "UI / React", "Zone / RTV"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md

## Source

[[docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE|docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md]]

## Summary

This guide adds a compact, separate-window oscillator view for the **Level 1 raw astro axes**. It is designed to reduce chart clutter while making the candle-by-candle sky-state easier to read. Instead of reading the full text panel every time, this indicator plots the raw astro axes on a **0..100 oscillator scale**: Flow Impulse Friction Pressure Transition MoonTempo SaturnDrag The default compact layout keeps only the four most important axes visible: Flow Impulse Friction Pressure The other three are available through inputs and are hidden by default to keep the subwindow clean. Use the same CSV time contract already established for EXP0013: the CSV already contains `broker_time` chart candle open time is matched directly against `broker_time` there must be **no second GMT shift** inside the oscillator logic If the CSV was built with broker GMT+3 already baked into `broker_time`, then

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Raw Axes Oscillator
  - File
  - Goal
  - Time contract
  - Default reading model
    - 1) Breakout / impulse reading
    - 2) Smooth continuation reading
    - 3) Dirty / noisy movement risk
  - Quick reading cheat sheet
  - Suggested compact setup
  - Compile and attach
  - How to use together with the text panel

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_time_contract_no_second_gmt_shift/dff6c2da3787_ASTRO_NO_SECOND_GMT_SHIFT|ASTRO_NO_SECOND_GMT_SHIFT.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE|ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md]] — score `18`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_EA_GUIDE|ASTRO_UNIFIED_DASHBOARD_EA_GUIDE.md]] — score `18`
- [[docs/evidence/run_exp0013_astro_raw_axes_oscillator/1cf21803c17b_RUN_ASTRO_RAW_AXES_OSCILLATOR|RUN_ASTRO_RAW_AXES_OSCILLATOR.md]] — score `18`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `17`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
