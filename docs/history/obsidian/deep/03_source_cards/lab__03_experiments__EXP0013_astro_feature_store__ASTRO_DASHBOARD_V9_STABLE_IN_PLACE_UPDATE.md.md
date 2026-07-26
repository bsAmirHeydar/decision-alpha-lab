
---
type: source_card
source_path: "docs/evidence/exp0013_astro_dashboard_stable_in_place_updates/ce83846c8724_ASTRO_DASHBOARD_V9_STABLE_IN_PLACE_UPDATE.md"
source_ext: ".md"
source_size: 1399
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_DASHBOARD_V9_STABLE_IN_PLACE_UPDATE.md

## Source

[[docs/evidence/exp0013_astro_dashboard_stable_in_place_updates/ce83846c8724_ASTRO_DASHBOARD_V9_STABLE_IN_PLACE_UPDATE|docs/evidence/exp0013_astro_dashboard_stable_in_place_updates/ce83846c8724_ASTRO_DASHBOARD_V9_STABLE_IN_PLACE_UPDATE.md]]

## Summary

This patch fixes the most important UI behavior problem: > The dashboard was fully deleting and rebuilding all objects on every timer refresh. That made the whole panel feel like it was resetting instead of simply updating the numbers. Every `OnTimer()` render did: This caused: flicker full layout reset buttons looking like they refresh constantly visual instability unnecessary object churn Normal timer refresh does **in-place update only**: Full cleanup/rebuild only happens when it is actually needed: EA init EA deinit chart resize/change user clicks a mode/layout button user toggles text or oscillator panel On each candle / timer refresh, the dashboard should remain visually stable. Only the metric values, status values, bars, and small oscillator points should update. For this dashboard, the shape/layout is static most of the time. The only dynamic part is the astro state for the curr

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Dashboard V9 - Stable In-Place Updates
  - What changed
    - Before
    - Now
  - Practical effect
  - Why this is the right behavior

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `12`
- [[docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX|ASTRO_CSV_RUNTIME_PATH_FIX.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `12`
- [[docs/evidence/exp0013_astro_dashboard_header_buttons_dynamic_spacing/38dfe94afabd_ASTRO_DASHBOARD_V8_HEADER_BUTTONS_DYNAMIC_SPACING|ASTRO_DASHBOARD_V8_HEADER_BUTTONS_DYNAMIC_SPACING.md]] — score `12`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO_DOCTRINE_V1.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|ASTRO_FEATURE_MEANING.md]] — score `12`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
