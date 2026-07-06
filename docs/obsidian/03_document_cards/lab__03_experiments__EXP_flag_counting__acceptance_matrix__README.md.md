---
title: "Phoenix Flag Counting Acceptance Matrix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP_flag_counting/acceptance_matrix/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "953"
concepts:
  - "F-Counting"
  - "MQL Native"
  - "Validation"
---


# Phoenix Flag Counting Acceptance Matrix

**Source:** [[lab/03_experiments/EXP_flag_counting/acceptance_matrix/README|lab/03_experiments/EXP_flag_counting/acceptance_matrix/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `953` bytes

## خلاصه

This folder documents Level 16 acceptance runs for `FlagCountingPhoenixExperiment.mq5`. Level 16 is implemented by: It runs after Level 15 postflight and before `FP_SUMMARY`. Enable CSV: Default output: Do not invent expected counts. Run baseline mode on a pinned symbol/timeframe/date-range, export `latest_acceptance.csv`, then copy real counts into the case registry and validation expected inputs.

## Headings

- Phoenix Flag Counting Acceptance Matrix
-   Modes
-   Output
-   Baseline policy

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/decision_locks/README|Flag Counting Phoenix Decision Locks]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/README|01 Concepts README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/README|Flag Counting Phoenix Rebuild]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
