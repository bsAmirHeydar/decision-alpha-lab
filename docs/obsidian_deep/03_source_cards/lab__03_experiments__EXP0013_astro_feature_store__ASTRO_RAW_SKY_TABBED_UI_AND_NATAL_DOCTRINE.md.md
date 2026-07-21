
---
type: source_card
source_path: "docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md"
source_ext: ".md"
source_size: 4082
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Convexity / Optionality", "Execution / Risk", "Licensing", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md

## Source

[[docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]]

## Summary

This patch cleans the raw sky dashboard by turning the UI into a tabbed cockpit. The previous version tried to show too many layers at the same time: bodies outer bodies aspects houses metrics dignity diagnostics orb strip That is useful for debugging, but bad for actual live reading. The dashboard now uses a strict separation: Instead of showing everything at once, the raw data is accessible through tabs: OVERVIEW BODIES ASPECTS HOUSES METRICS MINIMIZE RELOAD A compact snapshot: Sun / Moon Mercury / Venus Mars / Jupiter Saturn Moon phase ASC / MC if houses are available canonical metrics tightest aspects Use this for the first glance. The full planetary table: body zodiac position speed and direct/retrograde state declination house placement This is the raw sky map at the candle time. Aspect geometry sorted by tightest orb: pair aspect type orb applying/separating exact angular distance

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0013

## Headings

- EXP0013 Raw Sky Tabbed UI and Natal Doctrine
  - Why the previous raw dashboard was cluttered
  - V14 UI principle
  - Sections
    - OVERVIEW
    - BODIES
    - ASPECTS
    - HOUSES
    - METRICS
  - How to analyze astrology without pseudo-interpretation
  - Transit-only vs Natal + Transit
    - Transit-only

## Related Source Documents

- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `22`
- [[docs/evidence/exp0013_astro_raw_sky_radical_redesign/be7e95f4ddeb_ASTRO_RAW_SKY_RADICAL_REDESIGN|ASTRO_RAW_SKY_RADICAL_REDESIGN.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `20`
- [[docs/architecture|architecture.md]] — score `20`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `19`
- [[tools/astro_live_bridge/README|README.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|ASTRO_FEATURE_MEANING.md]] — score `18`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `18`
- [[docs/evidence/astro_professionalization_gap_map/b3f4b0da7c2e_ASTRO_PROFESSIONALIZATION_GAP_MAP|ASTRO_PROFESSIONALIZATION_GAP_MAP.md]] — score `18`
- [[docs/evidence/exp0013_pure_astro_signal_algorithms/7e6eca7a86f8_ASTRO_PURE_SIGNAL_ALGORITHMS|ASTRO_PURE_SIGNAL_ALGORITHMS.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
