---
title: "EXP0013 Astro Dashboard V4 - Layout Cleanup"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1758"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Execution"
  - "Structural Nodes"
---


# EXP0013 Astro Dashboard V4 - Layout Cleanup

**Source:** [[docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1758` bytes

## خلاصه

This patch focuses specifically on visual cleanup and readability. The previous interactive cockpit was functionally better, but visually it still had these problems: cards were too narrow value text and labels could collide header controls were too crowded diagnostics mixed into the same visual density as analytical cards oscillator rows were too compressed The header is now split into clearer lines: title research/runtime line symbol / timeframe / mode line row status line broker/utc line thesis/help line Buttons are now placed in two dedicated rows on the right side, instead of colliding with title text. Cards now use a wider structure with separate columns for: metric name numeric value

## Headings

- EXP0013 Astro Dashboard V4 - Layout Cleanup
-   What was fixed
-   V4 layout improvements
-     1) Cleaner header
-     2) Better card spacing
-     3) Clearer diagnostics
-     4) Cleaner oscillator
-   View modes
-     Cockpit mode
-     Focus mode
-   Buttons
-   Notes

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|EXP0013 Astro Time Contract and Panel Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_ui_review_redesign/3ba3ac6b98fa_ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN|EXP0013 Astro Dashboard V13 - UI Review and Redesign]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[docs/evidence/exp0013_astro_time_contract_no_second_gmt_shift/dff6c2da3787_ASTRO_NO_SECOND_GMT_SHIFT|EXP0013 Astro Time Contract: No Second GMT Shift]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|EXP0013 Astro Oscillator Compile Fix + Fractal Detail Plan]] — `experiment`
- [[docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE|EXP0013 Astro Raw Axes Oscillator]] — `experiment`
- [[docs/evidence/exp0013_astro_raw_sky_radical_redesign/be7e95f4ddeb_ASTRO_RAW_SKY_RADICAL_REDESIGN|EXP0013 Astro Raw Sky Radical Redesign]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
