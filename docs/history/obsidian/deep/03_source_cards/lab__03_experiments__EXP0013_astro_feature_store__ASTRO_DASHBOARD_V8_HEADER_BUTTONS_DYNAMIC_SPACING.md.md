
---
type: source_card
source_path: "docs/evidence/exp0013_astro_dashboard_header_buttons_dynamic_spacing/38dfe94afabd_ASTRO_DASHBOARD_V8_HEADER_BUTTONS_DYNAMIC_SPACING.md"
source_ext: ".md"
source_size: 926
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_DASHBOARD_V8_HEADER_BUTTONS_DYNAMIC_SPACING.md

## Source

[[docs/evidence/exp0013_astro_dashboard_header_buttons_dynamic_spacing/38dfe94afabd_ASTRO_DASHBOARD_V8_HEADER_BUTTONS_DYNAMIC_SPACING|docs/evidence/exp0013_astro_dashboard_header_buttons_dynamic_spacing/38dfe94afabd_ASTRO_DASHBOARD_V8_HEADER_BUTTONS_DYNAMIC_SPACING.md]]

## Summary

This patch specifically improves the three visual issues requested: larger main title clearer vertical separation between title, view line, CSV status, and time line a dedicated status badge for EXACT / FALLBACK / NOT FOUND better use of empty header space larger width and height more spacing between buttons clearer visibility in the top-right area label/value spacing is now based on the longest metric name in the section then extra visual gap is added after the label column value, bucket, and bar columns are separated more clearly same dynamic spacing logic is also applied to the compact oscillator low = red mid = yellow high = green Previous dashboard objects are still force-cleared on init, rerender, and deinit.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Dashboard V8 - Header, Buttons, Dynamic Spacing
  - 1) Clearer header
  - 2) Bigger buttons
  - 3) Better spacing inside cards
  - Visual logic
  - Cleanup

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|ASTRO_FEATURE_MEANING.md]] — score `14`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `14`
- [[docs/evidence/exp0013_astro_raw_sky_radical_redesign/be7e95f4ddeb_ASTRO_RAW_SKY_RADICAL_REDESIGN|ASTRO_RAW_SKY_RADICAL_REDESIGN.md]] — score `14`
- [[docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `14`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `14`
- [[docs/evidence/exp0013_astro_unified_dashboard_ea_display_update_fix/da2c2a4d4bf4_ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX|ASTRO_UNIFIED_DASHBOARD_DISPLAY_FIX.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
