---
title: "Visualization API Contract"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/ui/VISUALIZATION_API.md"
source_ext: ".md"
category: "ui_docs"
source_size_bytes: "5226"
entities:
  - "EXP0001"
  - "H0001"
  - "H0002"
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Visualization API Contract

**Source:** [[docs/ui/VISUALIZATION_API|docs/ui/VISUALIZATION_API.md]]

**Category:** `ui_docs`  
**Status:** ok  
**Size:** `5226` bytes

## خلاصه

This document defines the data contract between the Python research backend and the React visual terminal. Every metric and experiment must describe its visual output using these generic contracts instead of building metric-specific UI components. A replay visualization response should return: Allowed `source` values: The chart must render candles from this contract only. Allowed layer types: A table row must include a `selection_ref`: Selection must be deterministic and bidirectional. M0001 must eventually provide an adapter that maps metric output rows into: The metric itself should not import UI code. The adapter lives in `apps/api/app/services/visualization_mapper.py` or a metric-specifi

## Headings

- Visualization API Contract
-   Purpose
-   Top-Level Response
-   Dataset Descriptor
-   Candle Contract
-   Overlay Layer Contract
-   Marker Object
-   Zone Object
-   Event Window Object
-   Table Contract
-   Selection Map
-   Inspector Payload

## Entities

`EXP0001`, `H0001`, `H0002`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/ui/ROADMAP|UI Implementation Roadmap]] — `ui_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility|H0002 — Reversal vs Continuation Node-Exit Volatility Model]] — `hypothesis`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
