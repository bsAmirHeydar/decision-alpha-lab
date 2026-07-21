
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE.md"
source_ext: ".md"
source_size: 2455
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_CSV_DIAGNOSTIC_GUIDE.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE.md]]

## Summary

This guide explains how the runtime diagnostic separates file-path errors from CSV-content and timestamp-alignment errors. MQL5 does not read files from the repository root. When an input says: MQL resolves it as: Use MetaTrader: Then put the CSV under: The `.xlsx` workbook is human-review only. The runtime reader consumes the `.csv` mirror. Meaning: The EA could not open the file at the resolved runtime path. Fix: Meaning: Fix: regenerate the CSV and copy it again to the MT5 Data Folder. Meaning: Required columns: This often happens when the input points to the `.xlsx` file or to a wrong CSV. Meaning: Check: Meaning: The diagnostic panel will show: If requested time is outside CSV range, regenerate CSV for the tester/live date range. If requested time is inside range but exact match fails, check: For visual debugging only, set: For final research, restore exact matching after fixing tim

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro CSV Runtime Diagnostic Guide
  - Runtime Root
  - Diagnostic Stages
    - FILE_OPEN_FAILED
    - EMPTY_FILE / HEADER_READ_FAILED
    - BAD_HEADER
    - NO_VALID_ROWS
    - LOAD_OK but ROW NOT FOUND

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `16`
- [[docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX|ASTRO_CSV_RUNTIME_PATH_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `16`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO_DOCTRINE_V1.md]] — score `16`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `16`
- [[docs/evidence/exp0013_astro_time_contract_no_second_gmt_shift/dff6c2da3787_ASTRO_NO_SECOND_GMT_SHIFT|ASTRO_NO_SECOND_GMT_SHIFT.md]] — score `16`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `16`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|ASTRO_ONLY_EXECUTION_ROADMAP.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
