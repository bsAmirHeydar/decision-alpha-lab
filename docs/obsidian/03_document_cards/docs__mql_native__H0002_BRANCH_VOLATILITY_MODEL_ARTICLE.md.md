---
title: "H0002 — Reversal vs Continuation Branch Volatility Model"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "2346"
entities:
  - "H0001"
  - "H0002"
  - "H0003"
  - "M0001"
  - "M0002"
concepts:
  - "AI Agent Layer"
  - "NDS Anatomy"
  - "Validation"
---


# H0002 — Reversal vs Continuation Branch Volatility Model

**Source:** [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `2346` bytes

## خلاصه

H0002 classifies exact H0001/M0001 completed node-territory events into two node-side branches at the completed exit candle: reversal and continuation. The measurement remains locked to the original M0001 event RTV window. The branch label never changes the measured volatility window. For a LOW node, a completed exit close above the node price is `REVERSAL_AFTER_EXIT`, and a completed exit close below the node price is `CONTINUATION_AFTER_EXIT`. For a HIGH node, the mapping is inverted: a close below the node price is reversal, and a close above the node price is continuation. The emerging model is not merely “which branch is higher.” It has four dimensions: 1. Frequency: reversal is the hig

## Headings

- H0002 — Reversal vs Continuation Branch Volatility Model
-   Abstract
-   Branch definition
-   Branch model
-   Reporting
-   Interpretation
-   Relation to H0003

## Entities

`H0001`, `H0002`, `H0003`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001 / H0001 Logic Repair Audit]] — `mql_native_docs`
- [[docs/mql_native/M0003_CLUSTER_STRESS_LOCK|M0003 Cluster Stress Lock]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
