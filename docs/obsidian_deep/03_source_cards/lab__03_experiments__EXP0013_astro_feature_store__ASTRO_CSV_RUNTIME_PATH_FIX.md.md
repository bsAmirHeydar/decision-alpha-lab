
---
type: source_card
source_path: "docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX.md"
source_ext: ".md"
source_size: 2796
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_CSV_RUNTIME_PATH_FIX.md

## Source

[[docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX|docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX.md]]

## Summary

MQL5 does not read the `.xlsx` workbook at runtime. The workbook is only for human review. The Expert Advisor reads the CSV mirror. Human review file: MQL runtime CSV source inside the repo: MQL runtime CSV destination inside the actual MetaTrader data folder: The input must be the relative path from `MQL5/Files`: Do not use the repo path as the Expert input. The first line must be a readable CSV header containing fields such as: If the first bytes look like `PK`, the file is an XLSX/ZIP workbook and is not the runtime CSV. Open MetaTrader: Copy the displayed folder path and paste it into `$Mt5DataFolder` below. Use these inputs: For Strategy Tester, the Expert now includes: This property is literal and compile-time. The CSV must exist under `MQL5/Files/astro/` before running the test. The generated file starts at: Do not run the visual tester before this date unless you generate a wider

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Astro CSV Runtime Path Fix
  - Important distinction
  - Quick PowerShell check from repository root
  - Copy the runtime CSV into MetaTrader
  - Expert inputs
  - Date-range rule

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `16`
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
