---
title: "EXP0013 Astro Dashboard V2 - Cockpit Layout"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "2704"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# EXP0013 Astro Dashboard V2 - Cockpit Layout

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `2704` bytes

## خلاصه

This version replaces the crowded single oscillator cloud with a cockpit layout. The EA is research-only: no orders no iCustom no indicator path dependency no xlsx reading in MQL reads only runtime CSV draws text/cards directly with chart objects The dashboard does not delete and recreate all objects on every refresh. It updates the existing objects in-place. This avoids: flicker cut/return effect unstable live rendering overlapping text from stale labels Default professional layout: header/status card Path Quality card Micro M1 card Regime Engine card Macro Background card Prioritizes the smallest meaningful layer: Micro M1 Path Quality Regime Raw Axes Uses the older single preset text pane

## Headings

- EXP0013 Astro Dashboard V2 - Cockpit Layout
-   Main EA
-   Why the display is more stable
-   View modes
-     ASTRO_VIEW_COCKPIT
-     ASTRO_VIEW_MICRO_FOCUS
-     ASTRO_VIEW_SINGLE_PRESET
-   Recommended live inputs
-   Recommended historical/tester inputs
-   Reading order
-     1) Header verdict
-     2) Path Quality

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|EXP0013 Astro Fractal M1 Oscillator Guide]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|EXP0013 Astro Oscillator Compile Fix + Fractal Detail Plan]] — `experiment`
- [[docs/evidence/astro_professionalization_gap_map/b3f4b0da7c2e_ASTRO_PROFESSIONALIZATION_GAP_MAP|Astro Professionalization Gap Map]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
