---
title: "M0002 Deep Audit and Stability Suite"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "3174"
entities:
  - "H0001"
  - "H0002"
  - "M0001"
  - "M0002"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0002 Deep Audit and Stability Suite

**Source:** [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `3174` bytes

## خلاصه

This patch hardens the second hypothesis after the H0001/H0002 logic repair. H0002 does **not** ask whether an event hunted or touched. It asks only: > At the candle where the exit-gap window is completed, where did the close finish relative to the original node price? For LOW nodes: `close > node_price` => `REVERSAL_AFTER_EXIT` `close < node_price` => `CONTINUATION_AFTER_EXIT` For HIGH nodes: `close < node_price` => `REVERSAL_AFTER_EXIT` `close > node_price` => `CONTINUATION_AFTER_EXIT` The measured value is locked to the native M0001 event RTV: The branch is only a label. It does not move the volatility window. `nodes` is the count of confirmed structural pivot nodes. `m0001Events` is the

## Headings

- M0002 Deep Audit and Stability Suite
-   Purpose
-   Why m0001Events can be much larger than nodes
-   Random null engine
-   H2 stability suite
-   Logic repair v1.70

## Entities

`H0001`, `H0002`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001 / H0001 Logic Repair Audit]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
