
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK.md"
source_ext: ".md"
source_size: 1112
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Execution / Risk", "MQL Native", "Python Brain"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_CSV_FILES_ROOT_FALLBACK.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK.md]]

## Summary

This patch makes the Astro CSV reader accept both common runtime layouts: and: The input may be either: or: The loader now tries three paths in order: the exact input path the root `MQL5\Files` file name the canonical `MQL5\Files\astro` file name For Strategy Tester, both tester files are declared: This means the tester can copy the CSV whether it was placed directly in `Files` or inside `Files\astro`. If the panel still says `FILE_OPEN_FAILED`, the CSV is not in the active terminal data folder used by that MetaTrader instance, or the tester agent has not refreshed. Restart the tester or remove/re-run the test so it co…

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

## Entities

EXP0013

## Headings

- EXP0013 Astro CSV Runtime Path Fix

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `16`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `16`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `16`
- [[tools/astro_live_bridge/README|README.md]] — score `15`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] — score `14`
- [[docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX|ASTRO_CSV_RUNTIME_PATH_FIX.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
