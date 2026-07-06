---
title: "Phoenix Flag Counting Validation Cases"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP_flag_counting/validation_cases/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1606"
concepts:
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Phoenix Flag Counting Validation Cases

**Source:** [[lab/03_experiments/EXP_flag_counting/validation_cases/README|lab/03_experiments/EXP_flag_counting/validation_cases/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1606` bytes

## خلاصه

This folder stores Level 13 validation baselines for the Phoenix flag-counting engine. Level 13 does not invent expected counts. The workflow is: 1. Pick a case id from `docs/flag_counting/VALIDATION_CASE_REGISTRY.md`. 2. Pin broker symbol, timeframe, bar count/range, MT5 build, Phoenix inputs, and source commit. 3. Run `FlagCountingPhoenixExperiment.mq5` with export and validation enabled. 4. Save the generated CSV files from `MQL5/Files/FlagCountingPhoenix/` next to the case report. 5. Copy the accepted counts into the EA validation expected-min/max inputs for regression runs. Recommended case artifact names: A case is not frozen until it has a broker-valid range, expected counts, export f

## Headings

- Phoenix Flag Counting Validation Cases
-   Level 14 operational profiles

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/flag_counting/VALIDATION_CASE_REGISTRY|Flag Counting Validation Case Registry]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
