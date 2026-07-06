---
title: "M0001 Fast Final-Only Runtime"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1733"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Fast Final-Only Runtime

**Source:** [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1733` bytes

## خلاصه

Version: 1.59 The fast default keeps the research loop light while preserving the final chart drawings. On each intra-candle tick: When a new candle opens: No heavy full-history recomputation happens during the run when `InpRuntimeVisuals=false`. `OnDeinit` computes the complete state once: The same computed arrays are used for: 1. final `DAL_M0001_FINAL_NODES` report, 2. final `DAL_M0001_FINAL_RANDOM` report, 3. final restored chart drawings. This avoids duplicate logic and prevents drift between the final report and the chart. structural node arrows, local node price labels, live/revisited/consumed zones, true revisit labels, pending/live/revisited/consumed state labels, consumed markers,

## Headings

- M0001 Fast Final-Only Runtime
-   Default inputs
-   What happens during the run
-   What happens at shutdown
-   What is restored visually
-   What did not change

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
