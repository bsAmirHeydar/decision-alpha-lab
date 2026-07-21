---
title: "EXP0013 Astro Time Contract and Panel Fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1614"
entities:
  - "EXP0013"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Execution"
  - "MQL Native"
  - "Structural Nodes"
  - "Validation"
---


# EXP0013 Astro Time Contract and Panel Fix

**Source:** [[docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX|docs/evidence/exp0013_astro_time_contract_panel_fix/b3c4f9d25abb_ASTRO_TIME_CONTRACT_AND_PANEL_FIX.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1614` bytes

## خلاصه

When the Python builder is run with: the CSV contains two different time columns: MQL5 lookup must match the chart candle open time directly to `broker_time`. That means the GMT offset is **not applied to the lookup key**. The offset input is only used to validate and display the UTC contract: So if the CSV was generated with GMT+3, keep: Do **not** set it to zero. Setting it to zero would make the UTC validation wrong. MQL5 reads CSV files from the MT5 runtime file roots, not from the Git project root. The loader now tries both normal and common file roots: It also tries these filename layouts: Blank separator lines are no longer drawn as default `Label` objects. The panel skips empty lines

## Headings

- EXP0013 Astro Time Contract and Panel Fix
-   Core rule
-   Runtime path rule
-   Panel fix
-   Meaning of the displayed times

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FEATURE_MEANING|EXP0013 — Astro Feature Meaning and Research Semantics]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_OSCILLATOR_COMPILE_FIX_AND_FRACTAL_PLAN|EXP0013 Astro Oscillator Compile Fix + Fractal Detail Plan]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[docs/evidence/exp0013_astro_dashboard_layout_cleanup/fdcb3b9b6858_ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|EXP0013 Astro Dashboard V4 - Layout Cleanup]] — `experiment`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|EXP0013 Astro Fractal M1 Oscillator Guide]] — `experiment`
- [[docs/evidence/exp0013_astro_time_contract_no_second_gmt_shift/dff6c2da3787_ASTRO_NO_SECOND_GMT_SHIFT|EXP0013 Astro Time Contract: No Second GMT Shift]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|EXP0013 Astro-Only Execution Roadmap]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
