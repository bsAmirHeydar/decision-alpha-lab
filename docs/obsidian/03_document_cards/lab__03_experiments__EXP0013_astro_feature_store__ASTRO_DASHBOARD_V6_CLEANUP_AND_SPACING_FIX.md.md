---
title: "EXP0013 Astro Dashboard V6 - Cleanup and Spacing Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1710"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
---


# EXP0013 Astro Dashboard V6 - Cleanup and Spacing Fix

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1710` bytes

## خلاصه

This patch addresses two specific problems from the previous versions: When the expert refreshed, changed mode, or was reloaded, some previous panels stayed on the chart. That created duplicates such as: old focus cards still visible old cockpit cards staying behind old oscillator fragments remaining This version now does two levels of cleanup: full cleanup on `OnInit` full cleanup on `OnDeinit` full cleanup at the start of every render cycle It also removes objects from older EXP0013 astro prefixes, so legacy panels from previous dashboard versions are cleared too. The previous layout still had: labels too close to values values too close to state labels bars too close to text bottom oscill

## Headings

- EXP0013 Astro Dashboard V6 - Cleanup and Spacing Fix
-   1) Old panels were not being cleared
-     Problem
-     Fix
-   2) Text and numbers were still too crowded
-     Problem
-     Fix
-   Color logic
-   Modes
-     Cockpit
-     Focus
-   Notes

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V10_SPACING_HEADER_TUNE|EXP0013 Astro Dashboard V10 - Header and spacing tuning]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V11_BEST_VERSION|EXP0013 Astro Dashboard V11 - Best Version]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN|EXP0013 Astro Dashboard V13 - UI Review and Redesign]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|EXP0013 Astro Dashboard V4 - Layout Cleanup]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V7_VISUAL_POLISH|EXP0013 Astro Dashboard V7 - Visual Polish]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V8_HEADER_BUTTONS_DYNAMIC_SPACING|EXP0013 Astro Dashboard V8 - Header, Buttons, Dynamic Spacing]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
