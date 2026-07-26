
---
type: source_card
source_path: "lab/03_experiments/EXP_flag_counting/acceptance_matrix/README.md"
source_ext: ".md"
source_size: 953
empty: false
generated_at: 2026-07-06
concepts: ["Flag Counting", "MQL Native", "Python Brain", "Validation / Audit"]
entities: []
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP_flag_counting/acceptance_matrix/README|lab/03_experiments/EXP_flag_counting/acceptance_matrix/README.md]]

## Summary

This folder documents Level 16 acceptance runs for `FlagCountingPhoenixExperiment.mq5`. Level 16 is implemented by: It runs after Level 15 postflight and before `FP_SUMMARY`. Enable CSV: Default output: Do not invent expected counts. Run baseline mode on a pinned symbol/timeframe/date-range, export `latest_acceptance.csv`, then copy real counts into the case registry and validation expected inputs.

## Concepts

[[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Acceptance Matrix
  - Modes
  - Output
  - Baseline policy

## Related Source Documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `14`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_01_NO_SEND_CONTEXT|FLAG_COUNTING_CONSOLIDATION_PATCH_01_NO_SEND_CONTEXT.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_02_FINAL_DECISION_STATE|FLAG_COUNTING_CONSOLIDATION_PATCH_02_FINAL_DECISION_STATE.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION|FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
