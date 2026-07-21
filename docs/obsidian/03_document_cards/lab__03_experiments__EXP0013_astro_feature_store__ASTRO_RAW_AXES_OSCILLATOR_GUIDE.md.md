---
title: "EXP0013 Astro Raw Axes Oscillator"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "4526"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
  - "Execution"
  - "MQL Native"
  - "Structural Nodes"
---


# EXP0013 Astro Raw Axes Oscillator

**Source:** [[docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE|docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `4526` bytes

## خلاصه

This guide adds a compact, separate-window oscillator view for the **Level 1 raw astro axes**. It is designed to reduce chart clutter while making the candle-by-candle sky-state easier to read. Instead of reading the full text panel every time, this indicator plots the raw astro axes on a **0..100 oscillator scale**: Flow Impulse Friction Pressure Transition MoonTempo SaturnDrag The default compact layout keeps only the four most important axes visible: Flow Impulse Friction Pressure The other three are available through inputs and are hidden by default to keep the subwindow clean. Use the same CSV time contract already established for EXP0013: the CSV already contains `broker_time` chart ca

## Headings

- EXP0013 Astro Raw Axes Oscillator
-   File
-   Goal
-   Time contract
-   Default reading model
-     1) Breakout / impulse reading
-     2) Smooth continuation reading
-     3) Dirty / noisy movement risk
-   Quick reading cheat sheet
-   Suggested compact setup
-   Compile and attach
-   How to use together with the text panel

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/evidence/exp0013_astro_time_contract_no_second_gmt_shift/dff6c2da3787_ASTRO_NO_SECOND_GMT_SHIFT|EXP0013 Astro Time Contract: No Second GMT Shift]] — `experiment`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|EXP0013 Astro Time Contract and Panel Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|EXP0013 Astro Dashboard V4 - Layout Cleanup]] — `experiment`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
