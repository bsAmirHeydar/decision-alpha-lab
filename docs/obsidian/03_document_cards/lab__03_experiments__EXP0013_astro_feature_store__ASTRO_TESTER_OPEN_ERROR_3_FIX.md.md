---
title: "EXP0013 Tester open error [3] fix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TESTER_OPEN_ERROR_3_FIX.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "3524"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# EXP0013 Tester open error [3] fix

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TESTER_OPEN_ERROR_3_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TESTER_OPEN_ERROR_3_FIX.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `3524` bytes

## خلاصه

This is not an astro-calculation problem and not a CSV problem. It means the Strategy Tester is trying to load a **folder path** under `Indicators\Research\` as if it were an **Expert Advisor file**. In other words, the tester was pointed at: instead of a compiled `.ex5` file. Windows/MQL error `3` means: For this case the practical cause is usually one of these: the tester is in Expert mode while an indicator folder was selected the selected item is `Indicators\Research\` instead of an actual indicator file the indicator was not compiled into `.ex5` Shared Projects added an extra nested path and the selected tester path became ambiguous There are two correct ways to run this research visual

## Headings

- EXP0013 Tester open error [3] fix
-   Error
-   Meaning
-   Correct runtime roles
-     Option A — run the indicator directly
-     Option B — run the tester host EA
-   Added safety files
-   Correct compile order
-   Correct Strategy Tester selection
-   CSV input
-   Important

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|EXP0013 Astro Fractal M1 Oscillator Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PROFESSIONALIZATION_GAP_MAP|Astro Professionalization Gap Map]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PURE_SIGNAL_ALGORITHMS|EXP0013 Pure Astro Signal Algorithms]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_EA_GUIDE|EXP0013 Unified Dashboard EA]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|EXP0013 — Astro Excel / CSV Build Commands]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
