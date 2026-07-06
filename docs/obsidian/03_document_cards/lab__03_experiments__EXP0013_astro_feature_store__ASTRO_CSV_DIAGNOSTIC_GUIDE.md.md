---
title: "EXP0013 Astro CSV Runtime Diagnostic Guide"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "2455"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# EXP0013 Astro CSV Runtime Diagnostic Guide

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `2455` bytes

## خلاصه

This guide explains how the runtime diagnostic separates file-path errors from CSV-content and timestamp-alignment errors. MQL5 does not read files from the repository root. When an input says: MQL resolves it as: Use MetaTrader: Then put the CSV under: The `.xlsx` workbook is human-review only. The runtime reader consumes the `.csv` mirror. Meaning: The EA could not open the file at the resolved runtime path. Fix: Meaning: Fix: regenerate the CSV and copy it again to the MT5 Data Folder. Meaning: Required columns: This often happens when the input points to the `.xlsx` file or to a wrong CSV. Meaning: Check: Meaning: The diagnostic panel will show: If requested time is outside CSV range, re

## Headings

- EXP0013 Astro CSV Runtime Diagnostic Guide
-   Runtime Root
-   Diagnostic Stages
-     FILE_OPEN_FAILED
-     EMPTY_FILE / HEADER_READ_FAILED
-     BAD_HEADER
-     NO_VALID_ROWS
-     LOAD_OK but ROW NOT FOUND

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|EXP0013 Astro Fractal M1 Oscillator Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|Astro Professionalization Gap Map]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PURE_SIGNAL_ALGORITHMS|EXP0013 Pure Astro Signal Algorithms]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TESTER_OPEN_ERROR_3_FIX|EXP0013 Tester open error [3] fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_EA_GUIDE|EXP0013 Unified Dashboard EA]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|EXP0013 — Astro Excel / CSV Build Commands]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
