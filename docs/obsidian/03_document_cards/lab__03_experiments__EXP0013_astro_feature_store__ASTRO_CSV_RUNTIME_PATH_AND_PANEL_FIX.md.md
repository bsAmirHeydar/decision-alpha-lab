---
title: "EXP0013 Astro CSV Runtime Path and Panel Diagnostics"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1972"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Execution"
  - "MQL Native"
---


# EXP0013 Astro CSV Runtime Path and Panel Diagnostics

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1972` bytes

## خلاصه

This note explains the two separate failure classes used by the EXP0013 visual tester demos. If the panel shows: then the Expert Advisor did not even open the CSV. The problem is not astrology parsing and not timestamp alignment. The input: is resolved from the MetaTrader runtime Files root: In Strategy Tester, the diagnostic may show an Agent path such as: That means the tester agent did not receive the file. Put the CSV in the terminal data folder under `MQL5\Files\astro` before running the tester. The `#property tester_file` line can only package the file if it exists in the terminal `MQL5\Files` tree at test launch time. If the panel shows: then the file was opened, but its contents are

## Headings

- EXP0013 Astro CSV Runtime Path and Panel Diagnostics
-   1. File path / runtime access failure
-   2. CSV content failure
-   3. Timestamp lookup failure
-   Panel layout fix

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|EXP0013 Astro Oscillator Compile Fix + Fractal Detail Plan]] — `experiment`
- [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|EXP0013 Astro Time Contract and Panel Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|EXP0013 Astro Dashboard V4 - Layout Cleanup]] — `experiment`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
