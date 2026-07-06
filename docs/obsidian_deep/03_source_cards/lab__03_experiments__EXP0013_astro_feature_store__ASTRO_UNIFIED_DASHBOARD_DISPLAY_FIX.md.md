
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX.md"
source_ext: ".md"
source_size: 2270
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Execution / Risk", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX.md]]

## Summary

This patch improves the dashboard rendering quality and removes the visible cut/blink effect. The previous version used a full `DeleteByPrefix()` redraw on every render cycle. That caused: visible flicker / cut-and-return effect unstable live updates overlapping oscillator content because all metrics were drawn into one shared cloud long source-path text that pushed layout out of shape The dashboard now updates objects **in place**. Only stale oscillator point objects from the previous frame are deleted if they are no longer needed. This makes the panel much more stable in live mode. `OnTick()` no longer forces redraws. The UI is refreshed only from `OnTimer()`. This reduces jitter and prevents unnecessary re-rendering on every market tick. The previous oscillator was a single shared dot cloud. It is now a **row-based sparkline board**: one row per metric left-side label current numeric

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Unified Dashboard EA - Display and Update Fix
  - What was wrong before
  - What changed
    - 1) No more full delete on every refresh
    - 2) Timer-driven refresh only
    - 3) Row-based oscillator
    - 4) Cleaner text panel
  - Recommended settings
  - Reading model

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|ASTRO_FEATURE_MEANING.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_RADICAL_REDESIGN|ASTRO_RAW_SKY_RADICAL_REDESIGN.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `16`
- [[docs/research/H0009_astro_feature_taxonomy|H0009_astro_feature_taxonomy.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
