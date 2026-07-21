---
title: "H6 Candle-Stream Fast Optionality"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/H6_CANDLE_STREAM_FAST.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "1374"
entities:
  - "H0006"
  - "M0001"
  - "M0002"
concepts:
  - "Atomic No-Sample"
  - "Convexity"
  - "Known-Time Causality"
  - "Validation"
---


# H6 Candle-Stream Fast Optionality

**Source:** [[docs/debug/H6_CANDLE_STREAM_FAST|docs/debug/H6_CANDLE_STREAM_FAST.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `1374` bytes

## خلاصه

Release 108 changes the standalone H0006 report from a heavy batch/edge-map workflow into a fast forward candle-stream workflow by default. Still atomic and no-sample. Still uses raw M0001 known-time batches. Still treats same-known-time events as simultaneous. Mixed reversal/continuation batches remain ambiguous and are skipped from pure H6 measurements. The H6 measurement starts only after the batch is known. Default engine: `CANDLE_FORWARD_STREAM`. For each pure known-time batch at bar `k`, H6 opens an observation at `k+1` using `NEXT_OPEN` by default. Then the engine walks candles forward once, updates active observations with each bar's high/low, and closes them when their horizon matur

## Headings

- H6 Candle-Stream Fast Optionality
-   Contract
-   Engine
-   Speed defaults
-   Key audit fields

## Entities

`H0006`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/H6_NODE_SURVIVAL_MAP|H6 Node Survival Map]] — `debug_docs`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6 Fast Accurate Optionality Report]] — `debug_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4 Atomic Full Stress + Human Context Diagnostics]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[docs/evidence/h0006_node_survival_edge_map/067470759816_H0006_reversal_explosive_optionality|H0006 — Node Survival Edge Map]] — `hypothesis`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/architecture|System Architecture]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
