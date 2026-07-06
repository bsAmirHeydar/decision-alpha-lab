
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TESTER_OPEN_ERROR_3_FIX.md"
source_ext: ".md"
source_size: 3524
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_TESTER_OPEN_ERROR_3_FIX.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TESTER_OPEN_ERROR_3_FIX|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_TESTER_OPEN_ERROR_3_FIX.md]]

## Summary

This is not an astro-calculation problem and not a CSV problem. It means the Strategy Tester is trying to load a **folder path** under `Indicators\Research\` as if it were an **Expert Advisor file**. In other words, the tester was pointed at: instead of a compiled `.ex5` file. Windows/MQL error `3` means: For this case the practical cause is usually one of these: the tester is in Expert mode while an indicator folder was selected the selected item is `Indicators\Research\` instead of an actual indicator file the indicator was not compiled into `.ex5` Shared Projects added an extra nested path and the selected tester path became ambiguous There are two correct ways to run this research visualizer. Compile: Then attach the compiled indicator to a chart or to the Visual Tester chart. Do **not** select the `Research` folder itself. Compile: Then select this file in Strategy Tester as the **E

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 Tester open error [3] fix
  - Error
  - Meaning
  - Correct runtime roles
    - Option A — run the indicator directly
    - Option B — run the tester host EA
  - Added safety files
  - Correct compile order
  - Correct Strategy Tester selection
  - CSV input
  - Important

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_FIX|ASTRO_CSV_RUNTIME_PATH_FIX.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DOCTRINE_V1|ASTRO_DOCTRINE_V1.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_NO_SECOND_GMT_SHIFT|ASTRO_NO_SECOND_GMT_SHIFT.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
