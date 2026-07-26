
---
type: source_card
source_path: "docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE.md"
source_ext: ".md"
source_size: 1758
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Execution / Risk", "Path Smoothness", "UI / React", "Zone / RTV"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE.md

## Source

[[docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE.md]]

## Summary

This patch focuses specifically on visual cleanup and readability. The previous interactive cockpit was functionally better, but visually it still had these problems: cards were too narrow value text and labels could collide header controls were too crowded diagnostics mixed into the same visual density as analytical cards oscillator rows were too compressed The header is now split into clearer lines: title research/runtime line symbol / timeframe / mode line row status line broker/utc line thesis/help line Buttons are now placed in two dedicated rows on the right side, instead of colliding with title text. Cards now use a wider structure with separate columns for: metric name numeric value bucket label progress bar This makes them much easier to scan. Diagnostics now live in their own larger dedicated card. This keeps troubleshooting readable when the row is exact / fallback / missing.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Dashboard V4 - Layout Cleanup
  - What was fixed
  - V4 layout improvements
    - 1) Cleaner header
    - 2) Better card spacing
    - 3) Clearer diagnostics
    - 4) Cleaner oscillator
  - View modes
    - Cockpit mode
    - Focus mode
  - Buttons
  - Notes

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|ASTRO_FEATURE_MEANING.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN.md]] — score `16`
- [[docs/evidence/exp0013_astro_raw_axes_oscillator/d4d1fb06e8fa_ASTRO_RAW_AXES_OSCILLATOR_GUIDE|ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md]] — score `16`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `16`
- [[docs/research/H0009_astro_feature_taxonomy|H0009_astro_feature_taxonomy.md]] — score `15`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `14`
- [[docs/evidence/exp0013_astro_dashboard_ui_review_redesign/3ba3ac6b98fa_ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN|ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
