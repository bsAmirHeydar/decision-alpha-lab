---
title: "EXP0013 Astro Unified Dashboard EA - Display and Update Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "2270"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Execution"
  - "NDS Anatomy"
---


# EXP0013 Astro Unified Dashboard EA - Display and Update Fix

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `2270` bytes

## خلاصه

This patch improves the dashboard rendering quality and removes the visible cut/blink effect. The previous version used a full `DeleteByPrefix()` redraw on every render cycle. That caused: visible flicker / cut-and-return effect unstable live updates overlapping oscillator content because all metrics were drawn into one shared cloud long source-path text that pushed layout out of shape The dashboard now updates objects **in place**. Only stale oscillator point objects from the previous frame are deleted if they are no longer needed. This makes the panel much more stable in live mode. `OnTick()` no longer forces redraws. The UI is refreshed only from `OnTimer()`. This reduces jitter and preve

## Headings

- EXP0013 Astro Unified Dashboard EA - Display and Update Fix
-   What was wrong before
-   What changed
-     1) No more full delete on every refresh
-     2) Timer-driven refresh only
-     3) Row-based oscillator
-     4) Cleaner text panel
-   Recommended settings
-   Reading model

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_RADICAL_REDESIGN|EXP0013 Astro Raw Sky Radical Redesign]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|EXP0013 Raw Sky Tabbed UI and Natal Doctrine]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|EXP0013 Astro Dashboard V4 - Layout Cleanup]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
