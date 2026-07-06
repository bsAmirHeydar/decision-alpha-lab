---
title: "EXP0013 Astro Fractal M1 Oscillator Guide"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "5875"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# EXP0013 Astro Fractal M1 Oscillator Guide

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `5875` bytes

## خلاصه

This guide documents the detailed fractal oscillator layer for EXP0013. The goal is to observe the **quality of one-minute movement** without turning the chart into a text wall. The indicator is research-only. It does not trade, does not predict direction, and does not modify orders. `EXP0013_AstroFractalOscillator` is the new detailed one. The CSV can be placed in either location: The reader also tries MetaQuotes Common Files as a fallback: Recommended input: The CSV already contains `broker_time`, so the indicator matches chart candle open time directly against CSV `broker_time`. There is no second GMT shift. The indicator has several display presets. Each preset uses the same data but plo

## Headings

- EXP0013 Astro Fractal M1 Oscillator Guide
-   Indicator files
-   Runtime file rule
-   Presets
-     1. RAW AXES
-     2. MACRO BACKGROUND
-     3. REGIME ENGINE
-     4. MOON / MICRO M1
-     5. M1 PATH QUALITY
-     6. COMPACT JACKPOT
-   Fast reading models
-     Clean breakout window

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|Astro Professionalization Gap Map]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PURE_SIGNAL_ALGORITHMS|EXP0013 Pure Astro Signal Algorithms]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|EXP0013 — Astro Excel / CSV Build Commands]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_ROADMAP|EXP0013 Astro-Only Execution Roadmap]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|EXP0013 Astro Oscillator Compile Fix + Fractal Detail Plan]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
