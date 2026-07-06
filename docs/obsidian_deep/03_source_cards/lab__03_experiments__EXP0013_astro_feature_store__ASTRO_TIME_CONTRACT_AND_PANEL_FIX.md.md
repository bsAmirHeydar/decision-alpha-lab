
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md"
source_ext: ".md"
source_size: 1614
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TIME_CONTRACT_AND_PANEL_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]]

## Summary

When the Python builder is run with: the CSV contains two different time columns: MQL5 lookup must match the chart candle open time directly to `broker_time`. That means the GMT offset is **not applied to the lookup key**. The offset input is only used to validate and display the UTC contract: So if the CSV was generated with GMT+3, keep: Do **not** set it to zero. Setting it to zero would make the UTC validation wrong. MQL5 reads CSV files from the MT5 runtime file roots, not from the Git project root. The loader now tries both normal and common file roots: It also tries these filename layouts: Blank separator lines are no longer drawn as default `Label` objects. The panel skips empty lines and draws only meaningful lines, so the chart should not show stray `Label` text anymore. If the panel says: and `InpBrokerGmtOffsetHours = 3`, then the contract is correct: The market candle is matc

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXP0013

## Headings

- EXP0013 Astro Time Contract and Panel Fix
  - Core rule
  - Runtime path rule
  - Panel fix
  - Meaning of the displayed times

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|ASTRO_FEATURE_MEANING.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `20`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `20`
- [[docs/research/H0009_astro_feature_taxonomy|H0009_astro_feature_taxonomy.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_NO_SECOND_GMT_SHIFT|ASTRO_NO_SECOND_GMT_SHIFT.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
