---
title: "H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "5376"
entities:
  - "H0001"
  - "H0002"
  - "H0003"
  - "M0001"
  - "M0002"
  - "M0003"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity

**Source:** [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `5376` bytes

## خلاصه

H0003 asks whether the continuation branch discovered in H0002 is only a stronger event-volatility bucket, or whether it also creates a persistent post-event volatility regime. The question is deliberately not directional alpha yet. It is a volatility-state question: H0003 is downstream of the locked H0001/H0002 stack: 1. H0001 builds completed M0001 node-territory events. 2. H0001 event RTV is computed from the exact event window, with the final exit-gap candles excluded from RTV. 3. H0002 labels each completed event as reversal or continuation using the exit candle close relative to the original node price. 4. H0003 never rebuilds a separate event universe. It consumes exact M0001/M0002 br

## Headings

- H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity
-   Research question
-   Dependency chain
-   Branch definitions inherited from H0002
-   H0003 model
-   Stress tests
-   Current WTI M1 result snapshot
-   Current scientific statement
-   Important boundary
-   Completeness audit

## Entities

`H0001`, `H0002`, `H0003`, `M0001`, `M0002`, `M0003`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/M0003_CLUSTER_STRESS_LOCK|M0003 Cluster Stress Lock]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001 / H0001 Logic Repair Audit]] — `mql_native_docs`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
