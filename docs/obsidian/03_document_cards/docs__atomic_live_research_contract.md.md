---
title: "Atomic Live Research Contract"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/atomic_live_research_contract.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "3122"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Atomic Live Research Contract

**Source:** [[docs/atomic_live_research_contract|docs/atomic_live_research_contract.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `3122` bytes

## خلاصه

This document defines the strict contract used to prevent future leakage, fake sequencing, and non-tradable R statistics. For every decision candle `t`, the engine may only use information derived from closed candles up to `t`. Forbidden: using future-completed branch samples to decide at `t`, using a future outcome label before its known candle, ordering labels inside the same known candle, exiting on a regime change before that regime change is knowable. Required fields for any live-valid label: `known_index`, `known_time`, `source_event_id` or equivalent raw event reference, `energy_label`: reversal, continuation, or ambiguous, `direction_label` where applicable, `is_ambiguous`. All event

## Headings

- Atomic Live Research Contract
-   1. Decision-time contract
-   2. Same-candle batch contract
-   3. No-sample contract
-   4. Entry contract
-   5. R contract
-   6. Report contract

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[lab/02_hypotheses/H0005_directional_memory_atomic|H0005 — Directional Memory and Execution]] — `hypothesis`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[papers/001_atomic_live_regime_framework|Atomic Live Regime Framework]] — `paper`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001 Single-Source Live Architecture]] — `core_docs`
- [[docs/mql_live_visual_lab_debug_packages|M0001 Visual Debug Packages]] — `core_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
