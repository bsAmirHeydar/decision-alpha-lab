---
title: "MQL Module Map"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/MODULE_MAP.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "4688"
entities:
  - "H0001"
  - "H0002"
  - "H0003"
  - "H0004"
  - "M0001"
  - "M0002"
  - "M0003"
  - "M0004"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# MQL Module Map

**Source:** [[docs/mql_native/MODULE_MAP|docs/mql_native/MODULE_MAP.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `4688` bytes

## خلاصه

Version: 1.66 Removed legacy layers are intentionally not part of the active runtime: The M0001 MQL-native engine now includes a final-only professional validation layer: compact NODES/RANDOM reports, explicit effect-size metrics, paired validation, bootstrap confidence intervals, sign-flip permutation p-values, distribution-distance metrics, quantile/tail metrics, chronological split-stability metrics, optional parameter robustness, and an integrity audit. Histograms are optional (`InpPrintHistogram=false` by default) so Journal lines no longer truncate the core `COMPARE` metrics. See `docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS.md`. M0002 is isolated from M0001 at the EA and incl

## Headings

- MQL Module Map
-   v1.60 Professional Validation Metrics
-   v1.66 M0002 Neutral Reversal/Continuation EVENT_RTV Branch Lab
-   Logic repair v1.70
-   v1.00 M0004 Branch-Regime Clustering

## Entities

`H0001`, `H0002`, `H0003`, `H0004`, `M0001`, `M0002`, `M0003`, `M0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004 — Branch Regime Clustering]] — `hypothesis`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
