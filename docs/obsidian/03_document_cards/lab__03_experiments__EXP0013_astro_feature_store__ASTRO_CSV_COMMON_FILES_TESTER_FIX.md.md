---
title: "EXP0013 Astro CSV — Strategy Tester Common Files Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1476"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Execution"
  - "MQL Native"
---


# EXP0013 Astro CSV — Strategy Tester Common Files Fix

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1476` bytes

## خلاصه

MetaTrader has different runtime file roots: If the CSV is placed under the live terminal `MQL5\Files`, the visual tester may still fail with `FILE_OPEN_FAILED` because the EA is running inside a tester agent sandbox. This patch makes the reader try both: Put the CSV here: Then set the EA input to: The reader will first try the normal runtime `Files` root and then the Common `Files` root. `FILE_OPEN_FAILED` means the file was not opened at all. This is a path/runtime sandbox issue, not a CSV parsing issue. `BAD_HEADER` means the file was opened, but required columns such as `broker_time`, `utc_time`, or `feature_key` are missing. `NO_VALID_ROWS` means the header was found, but rows could not

## Headings

- EXP0013 Astro CSV — Strategy Tester Common Files Fix
-   Why the CSV can exist in `MQL5\Files` but still fail in Strategy Tester
-   Recommended stable setup
-   Diagnosis meanings

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
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
