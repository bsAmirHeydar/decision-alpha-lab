---
title: "H0004 — Reversal/Continuation Branch Regime Clustering"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "17438"
entities:
  - "H0001"
  - "H0002"
  - "H0003"
  - "H0004"
  - "M0001"
  - "M0002"
  - "M0004"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# H0004 — Reversal/Continuation Branch Regime Clustering

**Source:** [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `17438` bytes

## خلاصه

H0004 asks whether reversal and continuation are only independent labels on completed node-territory events, or whether they form branch regimes with inertia. Core question: This is different from H0003. H0003 tests volatility-memory inside each branch. H0004 tests memory of the branch labels themselves. H0004 is a regime-state hypothesis. H0004 uses the same locked event stack: 1. H0001 detects structural nodes and completed node-territory events. 2. H0001 computes exact event RTV. 3. H0002 labels each completed event as reversal or continuation. 4. H0004 sorts valid M0002 branch samples chronologically by outcome/exit index. 5. H0004 studies the branch-label sequence. No separate event bui

## Headings

- H0004 — Reversal/Continuation Branch Regime Clustering
-   Research question
-   Dependency chain
-   Null hypothesis
-   Primary metrics
-     Frequency model
-     Transition matrix
-     Lag correlation
-     Run clustering
-     Block concentration
-   Stress suite
-   Interpretation rules

## Entities

`H0001`, `H0002`, `H0003`, `H0004`, `M0001`, `M0002`, `M0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004 — Branch Regime Clustering]] — `hypothesis`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005 — Contextual Branch Regime State]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
