---
title: "EXP0013 Astro Dashboard V9 - Stable In-Place Updates"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V9_STABLE_IN_PLACE_UPDATE.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1399"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
---


# EXP0013 Astro Dashboard V9 - Stable In-Place Updates

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V9_STABLE_IN_PLACE_UPDATE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V9_STABLE_IN_PLACE_UPDATE.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1399` bytes

## خلاصه

This patch fixes the most important UI behavior problem: > The dashboard was fully deleting and rebuilding all objects on every timer refresh. That made the whole panel feel like it was resetting instead of simply updating the numbers. Every `OnTimer()` render did: This caused: flicker full layout reset buttons looking like they refresh constantly visual instability unnecessary object churn Normal timer refresh does **in-place update only**: Full cleanup/rebuild only happens when it is actually needed: EA init EA deinit chart resize/change user clicks a mode/layout button user toggles text or oscillator panel On each candle / timer refresh, the dashboard should remain visually stable. Only t

## Headings

- EXP0013 Astro Dashboard V9 - Stable In-Place Updates
-   What changed
-     Before
-     Now
-   Practical effect
-   Why this is the right behavior

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_FIX|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V10_SPACING_HEADER_TUNE|EXP0013 Astro Dashboard V10 - Header and spacing tuning]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V11_BEST_VERSION|EXP0013 Astro Dashboard V11 - Best Version]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V12_HEADER_MINIMIZE_CLEAN_OSC|EXP0013 Astro Dashboard V12 - Clean Header, Minimize Mode, Cleaner Oscillator]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN|EXP0013 Astro Dashboard V13 - UI Review and Redesign]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|EXP0013 Astro Dashboard V4 - Layout Cleanup]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
