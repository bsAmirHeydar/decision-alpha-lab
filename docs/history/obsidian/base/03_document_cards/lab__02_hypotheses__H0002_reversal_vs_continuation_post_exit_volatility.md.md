---
title: "H0002 — Reversal vs Continuation Node-Exit Volatility Model"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility.md"
source_ext: ".md"
category: "hypothesis"
source_size_bytes: "3227"
entities:
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


# H0002 — Reversal vs Continuation Node-Exit Volatility Model

**Source:** [[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility|lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility.md]]

**Category:** `hypothesis`  
**Status:** ok  
**Size:** `3227` bytes

## خلاصه

Status: active / fact-layer validation Given a valid completed M0001 structural-node event, does the completed exit side create different volatility regimes? H0002 uses the exact event stream created by H0001/M0001. It does not create a separate event builder. A valid H0002 sample must be: The node lifecycle, hunt/touch consume behavior, revisit reset, baseline logic, warmup handling, and exit-gap logic are inherited from M0001. The M0001 event exit is side-agnostic. A completed exit candle can be fully above or fully below the frozen event territory. The touch is confirmed only after `exit_gap` consecutive fully-outside candles. Exit is not equal to reversal. At the completed exit candle: T

## Headings

- H0002 — Reversal vs Continuation Node-Exit Volatility Model
-   Research question
-   Event source
-   Exit logic
-   Branch classifier
-   Measurement
-   Current working model
-     1. Frequency
-     2. Intensity
-     3. Tail
-     4. Post-event memory
-   Acceptance signature

## Entities

`H0001`, `H0002`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/ui/ROADMAP|UI Implementation Roadmap]] — `ui_docs`
- [[docs/ui/VISUALIZATION_API|Visualization API Contract]] — `ui_docs`
- [[README|Decision Alpha Lab]] — `readme`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
