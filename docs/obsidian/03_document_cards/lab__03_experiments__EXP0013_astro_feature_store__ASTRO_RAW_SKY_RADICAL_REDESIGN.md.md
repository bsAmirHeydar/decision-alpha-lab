---
title: "EXP0013 Astro Raw Sky Radical Redesign"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_RADICAL_REDESIGN.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "3177"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# EXP0013 Astro Raw Sky Radical Redesign

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_RADICAL_REDESIGN|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_RADICAL_REDESIGN.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `3177` bytes

## خلاصه

This patch removes the fake-looking interpretive layer from the live dashboard and turns the UI into a raw sky-map cockpit. The dashboard should not invent market meaning. It should show the astronomical state cleanly and let research decide what has distributional value. The new rule is: For each body: zodiac sign degree inside sign ecliptic longitude speed in longitude direct / retrograde state declination house placement if houses are available Signs are shown as exact zodiac placement, not as a market interpretation. Example: Aspects are shown by geometry only: pair nearest aspect class orb applying / separating exact angle The aspects card is sorted by tightest orb. House calculation is

## Headings

- EXP0013 Astro Raw Sky Radical Redesign
-   Principle
-   What the dashboard now shows
-     1) Bodies
-     2) Signs
-     3) Aspects
-     4) Houses
-   Location note for houses
-   Canonical raw metrics
-   UI modes
-   Important

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|EXP0013 — Astro Excel / CSV Build Commands]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|Astro Professionalization Gap Map]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|EXP0013 Raw Sky Tabbed UI and Natal Doctrine]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[docs/research/H0009_astro_feature_taxonomy|EXP0013 — Astro Feature Meaning and Research Semantics]] — `research_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|EXP0013 Astro Fractal M1 Oscillator Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|EXP0013 Astro Oscillator Compile Fix + Fractal Detail Plan]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PURE_SIGNAL_ALGORITHMS|EXP0013 Pure Astro Signal Algorithms]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TIME_CONTRACT_AND_PANEL_FIX|EXP0013 Astro Time Contract and Panel Fix]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
