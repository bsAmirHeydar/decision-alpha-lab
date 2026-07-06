
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX.md"
source_ext: ".md"
source_size: 1476
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Execution / Risk", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_CSV_COMMON_FILES_TESTER_FIX.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]]

## Summary

MetaTrader has different runtime file roots: If the CSV is placed under the live terminal `MQL5\Files`, the visual tester may still fail with `FILE_OPEN_FAILED` because the EA is running inside a tester agent sandbox. This patch makes the reader try both: Put the CSV here: Then set the EA input to: The reader will first try the normal runtime `Files` root and then the Common `Files` root. `FILE_OPEN_FAILED` means the file was not opened at all. This is a path/runtime sandbox issue, not a CSV parsing issue. `BAD_HEADER` means the file was opened, but required columns such as `broker_time`, `utc_time`, or `feature_key` are missing. `NO_VALID_ROWS` means the header was found, but rows could not be parsed. `ROW NOT FOUND` / lookup failure means the CSV was loaded but the current candle time was not found in the loaded date range.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro CSV — Strategy Tester Common Files Fix
  - Why the CSV can exist in `MQL5\Files` but still fail in Strategy Tester
  - Recommended stable setup
  - Diagnosis meanings

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `18`
- [[tools/astro_live_bridge/README|README.md]] — score `17`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|ASTRO_CSV_FILES_ROOT_FALLBACK.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_FIX|ASTRO_CSV_RUNTIME_PATH_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
