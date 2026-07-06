---
title: "EXP0013 Raw Sky V14 Compile Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_V14_COMPILE_FIX.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "544"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
  - "MQL Native"
---


# EXP0013 Raw Sky V14 Compile Fix

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_V14_COMPILE_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_V14_COMPILE_FIX.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `544` bytes

## خلاصه

This patch fixes the V14 `undeclared identifier` compile error in `EXP0013_AstroUnifiedDashboardEA.mq5`. The V14 tabbed raw-sky UI started using additional derived layout fields in `DAL_GetGrid()` and the tab renderers: `card_w` `diag_w` `col1_x` `col2_x` `col3_x` `row1_y` `row2_y` `row3_y` But those fields were not declared inside the `DAL_UIGrid` struct. The missing fields were added to `DAL_UIGrid`. No trading logic, astrology logic, or CSV contract was changed.

## Headings

- EXP0013 Raw Sky V14 Compile Fix
-   Cause
-   Fix

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_FIX|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|EXP0013 Astro Fractal M1 Oscillator Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_NO_SECOND_GMT_SHIFT|EXP0013 Astro Time Contract: No Second GMT Shift]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_ROADMAP|EXP0013 Astro-Only Execution Roadmap]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
