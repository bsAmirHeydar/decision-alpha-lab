---
title: "Phoenix Level 18 Static QA"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP_flag_counting/static_qa/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "872"
concepts:
  - "F-Counting"
  - "MQL Native"
---


# Phoenix Level 18 Static QA

**Source:** [[lab/03_experiments/EXP_flag_counting/static_qa/README|lab/03_experiments/EXP_flag_counting/static_qa/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `872` bytes

## خلاصه

Level 18 is the compile/static QA hardening layer after the official Level 17 decision lock. Run from repository root: Strict mode fails on warnings too: The scanner checks Phoenix MQL files for: empty `Print()` calls very long multi-argument `Print(...)` calls duplicate EA input names stale `phoenix_level16` / `phoenix_level17` identity pass references in MQL source stale interface contract versions stale short report aliases such as `r.export_forced` missing Level 18 modules The MQL runtime layer prints `FP_LEVEL18`; this Python scanner is the source-side companion for checks that cannot be proven from inside MQL5 at runtime.

## Headings

- Phoenix Level 18 Static QA

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]

## Related documents

- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/acceptance_matrix/README|Phoenix Flag Counting Acceptance Matrix]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/decision_locks/README|Flag Counting Phoenix Decision Locks]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/sections/03_entry_families/README|Entry Families Beyond Extreme]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
