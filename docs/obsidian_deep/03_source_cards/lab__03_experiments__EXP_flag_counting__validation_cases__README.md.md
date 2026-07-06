
---
type: source_card
source_path: "lab/03_experiments/EXP_flag_counting/validation_cases/README.md"
source_ext: ".md"
source_size: 1606
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP_flag_counting/validation_cases/README|lab/03_experiments/EXP_flag_counting/validation_cases/README.md]]

## Summary

This folder stores Level 13 validation baselines for the Phoenix flag-counting engine. Level 13 does not invent expected counts. The workflow is: Pick a case id from `docs/flag_counting/VALIDATION_CASE_REGISTRY.md`. Pin broker symbol, timeframe, bar count/range, MT5 build, Phoenix inputs, and source commit. Run `FlagCountingPhoenixExperiment.mq5` with export and validation enabled. Save the generated CSV files from `MQL5/Files/FlagCountingPhoenix/` next to the case report. Copy the accepted counts into the EA validation expected-min/max inputs for regression runs. Recommended case artifact names: A case is not frozen until it has a broker-valid range, expected counts, export files, screenshot, and notes explaining any intentional deviation from the previous baseline. Before baselining a case, choose one profile explicitly: For validation cases, prefer:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Validation Cases
  - Level 14 operational profiles

## Related Source Documents

- [[docs/flag_counting/VALIDATION_CASE_REGISTRY|VALIDATION_CASE_REGISTRY.md]] — score `24`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `18`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING|FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS|FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
