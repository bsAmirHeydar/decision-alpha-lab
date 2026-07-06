---
title: "Flag Counting Validation Case Registry"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/VALIDATION_CASE_REGISTRY.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4892"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Flag Counting Validation Case Registry

**Source:** [[docs/flag_counting/VALIDATION_CASE_REGISTRY|docs/flag_counting/VALIDATION_CASE_REGISTRY.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4892` bytes

## خلاصه

Status: active validation registry for Phoenix. Source of truth: `docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md`. This registry turns validation from visual opinion into deterministic baselines. Broker-specific symbol names and exact historical availability differ. Therefore a case has two states: Do not invent expected counts. The first accepted run for a pinned broker/range creates the baseline; later patches compare against it. Recommended output location: Recommended files per case: Purpose: Required status before Level 02 freeze: `baselined`. Purpose: Required status before Level 04 freeze: `baselined`. Purpose: Required status before Level 05 freeze: `baselined`. Purpose: Required

## Headings

- Flag Counting Validation Case Registry
-   Purpose
-   Baseline file naming
-   Required fields per baseline
-   Mandatory baseline cases
-     FC-GC-001 — Node plateau and equality
-     FC-GC-002 — Hook/ND branch size
-     FC-GC-003 — Bullish and bearish flag body
-     FC-GC-004 — F1 internal confirmation
-     FC-GC-005 — F2 backfill and size qualification
-     FC-GC-006 — F3 OR completion and lock
-     FC-GC-007 — Sequence ownership and duplicate hiding

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER|Flag Counting Level 19D — Closed-Bar Transition Event Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|Flag Counting Level 19Z — Complete Observation Suite]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|Flag Counting Level 20 — Entry Bridge / X-Y Anchor Join]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/05_validation/VAL001/report|Report]] — `validation`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|Flag Counting Concept Specification v2]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
