
---
type: source_card
source_path: "docs/evidence/exp0013_astro_raw_sky_radical_redesign/be7e95f4ddeb_ASTRO_RAW_SKY_RADICAL_REDESIGN.md"
source_ext: ".md"
source_size: 3177
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Convexity / Optionality", "Execution / Risk", "Known-Time Causality", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_RAW_SKY_RADICAL_REDESIGN.md

## Source

[[docs/evidence/exp0013_astro_raw_sky_radical_redesign/be7e95f4ddeb_ASTRO_RAW_SKY_RADICAL_REDESIGN|docs/evidence/exp0013_astro_raw_sky_radical_redesign/be7e95f4ddeb_ASTRO_RAW_SKY_RADICAL_REDESIGN.md]]

## Summary

This patch removes the fake-looking interpretive layer from the live dashboard and turns the UI into a raw sky-map cockpit. The dashboard should not invent market meaning. It should show the astronomical state cleanly and let research decide what has distributional value. The new rule is: For each body: zodiac sign degree inside sign ecliptic longitude speed in longitude direct / retrograde state declination house placement if houses are available Signs are shown as exact zodiac placement, not as a market interpretation. Example: Aspects are shown by geometry only: pair nearest aspect class orb applying / separating exact angle The aspects card is sorted by tightest orb. House calculation is optional and requires a location. If the CSV was built without location, the dashboard explicitly says houses are unavailable. To enable houses in the Python builder: For live bridge: Houses are not

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Raw Sky Radical Redesign
  - Principle
  - What the dashboard now shows
    - 1) Bodies
    - 2) Signs
    - 3) Aspects
    - 4) Houses
  - Location note for houses
  - Canonical raw metrics
  - UI modes
  - Important

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|ASTRO_FEATURE_MEANING.md]] — score `20`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `20`
- [[docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `20`
- [[docs/evidence/exp0013_astro_excel_csv_build_commands/6e29545f8168_BUILD_EXCEL_COMMANDS|BUILD_EXCEL_COMMANDS.md]] — score `20`
- [[docs/research/H0009_astro_feature_taxonomy|H0009_astro_feature_taxonomy.md]] — score `19`
- [[docs/evidence/astro_professionalization_gap_map/b3f4b0da7c2e_ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `18`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `18`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `17`
- [[tools/astro_live_bridge/README|README.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
