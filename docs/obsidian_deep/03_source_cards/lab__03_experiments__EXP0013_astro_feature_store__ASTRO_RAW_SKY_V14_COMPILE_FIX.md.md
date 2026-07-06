
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_V14_COMPILE_FIX.md"
source_ext: ".md"
source_size: 544
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_RAW_SKY_V14_COMPILE_FIX.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_V14_COMPILE_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_V14_COMPILE_FIX.md]]

## Summary

This patch fixes the V14 `undeclared identifier` compile error in `EXP0013_AstroUnifiedDashboardEA.mq5`. The V14 tabbed raw-sky UI started using additional derived layout fields in `DAL_GetGrid()` and the tab renderers: `card_w` `diag_w` `col1_x` `col2_x` `col3_x` `row1_y` `row2_y` `row3_y` But those fields were not declared inside the `DAL_UIGrid` struct. The missing fields were added to `DAL_UIGrid`. No trading logic, astrology logic, or CSV contract was changed.

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Raw Sky V14 Compile Fix
  - Cause
  - Fix

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_FIX|ASTRO_CSV_RUNTIME_PATH_FIX.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO_DOCTRINE_V1.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_NO_SECOND_GMT_SHIFT|ASTRO_NO_SECOND_GMT_SHIFT.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
