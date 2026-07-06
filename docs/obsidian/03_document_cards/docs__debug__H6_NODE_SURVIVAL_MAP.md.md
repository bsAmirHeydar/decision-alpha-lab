---
title: "H6 Node Survival Map"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/H6_NODE_SURVIVAL_MAP.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "1445"
entities:
  - "H0006"
  - "M0001"
  - "M0002"
concepts:
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# H6 Node Survival Map

**Source:** [[docs/debug/H6_NODE_SURVIVAL_MAP|docs/debug/H6_NODE_SURVIVAL_MAP.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `1445` bytes

## خلاصه

This release redefines H0006 as a chart-facing no-sample node survival map. A raw M0001 node becomes an edge-candidate level if, after its known-time candle, the market does not break that node price within the configured survival horizons. Default horizons: 20 candles: red 50 candles: green 100 candles: purple Contract: raw M0001 nodes only no M0002 branch samples no branch sample ordering no internal ordering among nodes known on the same candle node survival is measured only after known-time chart objects are deleted and redrawn using the `DAL_H6_NODE_` prefix Break definition: high node breaks when a later candle high reaches `node_price + break_buffer` low node breaks when a later candl

## Headings

- H6 Node Survival Map

## Entities

`H0006`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/H6_CANDLE_STREAM_FAST|H6 Candle-Stream Fast Optionality]] — `debug_docs`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6 Fast Accurate Optionality Report]] — `debug_docs`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4 Atomic Full Stress + Human Context Diagnostics]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[lab/02_hypotheses/H0006_reversal_explosive_optionality|H0006 — Node Survival Edge Map]] — `hypothesis`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
