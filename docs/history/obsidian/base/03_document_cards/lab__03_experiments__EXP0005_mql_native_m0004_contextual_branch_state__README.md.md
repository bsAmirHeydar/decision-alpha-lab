---
title: "EXP0005 — MQL-native contextual branch-state diagnostics"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0005_mql_native_m0004_contextual_branch_state/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "885"
entities:
  - "EXP0005"
concepts:
  - "MQL Native"
  - "Validation"
---


# EXP0005 — MQL-native contextual branch-state diagnostics

**Source:** [[lab/03_experiments/EXP0005_mql_native_m0004_contextual_branch_state/README|lab/03_experiments/EXP0005_mql_native_m0004_contextual_branch_state/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `885` bytes

## خلاصه

Run `M0004_BranchRegimeClustering.mq5` build 1.02 and inspect the contextual report lines. Required lines: Interpretation priority: 1. `dominantLiftPct` should be positive. 2. `conflictContextMinusLastPct` tells whether context beats last-only when they disagree. 3. Contextual lift must survive global and composite stratified shuffle nulls.

## Headings

- EXP0005 — MQL-native contextual branch-state diagnostics

## Entities

`EXP0005`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0005_mql_native_directional_memory/README|EXP0005 — MQL-native H0005 directional memory]] — `experiment`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/finalization/README|EXP0013 Finalization Snapshot]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/acceptance_matrix/README|Phoenix Flag Counting Acceptance Matrix]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/decision_locks/README|Flag Counting Phoenix Decision Locks]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
