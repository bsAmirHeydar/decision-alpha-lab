
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX.md"
source_ext: ".md"
source_size: 1710
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Path Smoothness", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX.md]]

## Summary

This patch addresses two specific problems from the previous versions: When the expert refreshed, changed mode, or was reloaded, some previous panels stayed on the chart. That created duplicates such as: old focus cards still visible old cockpit cards staying behind old oscillator fragments remaining This version now does two levels of cleanup: full cleanup on `OnInit` full cleanup on `OnDeinit` full cleanup at the start of every render cycle It also removes objects from older EXP0013 astro prefixes, so legacy panels from previous dashboard versions are cleared too. The previous layout still had: labels too close to values values too close to state labels bars too close to text bottom oscillator overly wide and visually noisy This version improves spacing by: increasing metric-row spacing separating columns into: label value state bucket bar widening the focus card and cockpit cards shri

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Dashboard V6 - Cleanup and Spacing Fix
  - 1) Old panels were not being cleared
    - Problem
    - Fix
  - 2) Text and numbers were still too crowded
    - Problem
    - Fix
  - Color logic
  - Modes
    - Cockpit
    - Focus
  - Notes

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V10_SPACING_HEADER_TUNE|ASTRO_DASHBOARD_V10_SPACING_HEADER_TUNE.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V11_BEST_VERSION|ASTRO_DASHBOARD_V11_BEST_VERSION.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN|ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `12`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V5_PRO_CLEAN_GUIDE|ASTRO_DASHBOARD_V5_PRO_CLEAN_GUIDE.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
