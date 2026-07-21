
---
type: source_card
source_path: "tools/astro_live_bridge/README.md"
source_ext: ".md"
source_size: 2891
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Convexity / Optionality", "Execution / Risk", "Licensing", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — README.md

## Source

[[tools/astro_live_bridge/README|tools/astro_live_bridge/README.md]]

## Summary

This bridge generates a small rolling astro CSV for the live MT5 dashboard. Python writes: `broker_time`: already aligned to the broker chart time `utc_time`: true UTC used for astronomical calculations MQL5 reads `broker_time` directly. There is no second GMT shift inside MQL. Written atomically into Common Files: The status JSON is for human/live diagnostics and includes: last update UTC output CSV path broker start/end window rows hint error text if generation failed The live bridge can pass house-location inputs to the builder: If `--house-lat` and `--house-lon` are omitted, the CSV remains geocentric-only and the MQL dashboard will show houses as unavailable. The live bridge can also build a rolling CSV that embeds a fixed natal or inception chart: When natal inputs are present, the rolling CSV contains: natal body state natal houses and angles transit-to-natal activations pure astr

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Live Bridge V2
  - Runtime contract
  - One-shot test
  - Continuous live mode
  - MT5 EA inputs
  - Output files
  - Optional house cusps
  - Optional natal or inception chart

## Related Source Documents

- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `21`
- [[docs/evidence/exp0013_raw_sky_tabbed_ui_natal_doctrine/4417b5ea0f1c_ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE|ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `19`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `17`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `17`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `17`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO_DOCTRINE_V1.md]] — score `17`
- [[docs/evidence/exp0013_astro_time_contract_no_second_gmt_shift/dff6c2da3787_ASTRO_NO_SECOND_GMT_SHIFT|ASTRO_NO_SECOND_GMT_SHIFT.md]] — score `17`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
