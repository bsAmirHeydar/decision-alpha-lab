---
title: "EXP0013 Raw Sky Tabbed UI and Natal Doctrine"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "4082"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Convexity"
  - "Execution"
  - "Licensing"
  - "NDS Anatomy"
---


# EXP0013 Raw Sky Tabbed UI and Natal Doctrine

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `4082` bytes

## خلاصه

This patch cleans the raw sky dashboard by turning the UI into a tabbed cockpit. The previous version tried to show too many layers at the same time: bodies outer bodies aspects houses metrics dignity diagnostics orb strip That is useful for debugging, but bad for actual live reading. The dashboard now uses a strict separation: Instead of showing everything at once, the raw data is accessible through tabs: OVERVIEW BODIES ASPECTS HOUSES METRICS MINIMIZE RELOAD A compact snapshot: Sun / Moon Mercury / Venus Mars / Jupiter Saturn Moon phase ASC / MC if houses are available canonical metrics tightest aspects Use this for the first glance. The full planetary table: body zodiac position speed and

## Headings

- EXP0013 Raw Sky Tabbed UI and Natal Doctrine
-   Why the previous raw dashboard was cluttered
-   V14 UI principle
-   Sections
-     OVERVIEW
-     BODIES
-     ASPECTS
-     HOUSES
-     METRICS
-   How to analyze astrology without pseudo-interpretation
-   Transit-only vs Natal + Transit
-     Transit-only

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_RADICAL_REDESIGN|EXP0013 Astro Raw Sky Radical Redesign]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|Astro Professionalization Gap Map]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PURE_SIGNAL_ALGORITHMS|EXP0013 Pure Astro Signal Algorithms]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX|EXP0013 Astro Unified Dashboard EA - Display and Update Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|EXP0013 — Astro Excel / CSV Build Commands]] — `experiment`
- [[docs/architecture|System Architecture]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
