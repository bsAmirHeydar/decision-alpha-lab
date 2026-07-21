---
title: "H0001 — Structural Node Territory Volatility"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "2815"
entities:
  - "H0001"
  - "H0002"
  - "H0003"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# H0001 — Structural Node Territory Volatility

**Source:** [[docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE|docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `2815` bytes

## خلاصه

H0001 tests whether completed structural-node territory events generate materially higher relative volatility than length-matched random windows. The production MQL-native definition is intentionally event-based and avoids directional assumptions: a node event begins when price first touches a frozen node territory and completes only after the configured `exit_gap` number of fully-outside candles. The exit can occur on either side of the frozen territory. 1. Detect confirmed structural highs and lows using the L-rule. A node becomes active only after the right-side confirmation window has closed. 2. Build a node territory from the node price and the current structural extreme. The territory

## Headings

- H0001 — Structural Node Territory Volatility
-   Abstract
-   Algorithm
-   Consumption lifecycle
-   Validation stack
-   Interpretation
-   Horizon half-life reporting guardrail

## Entities

`H0001`, `H0002`, `H0003`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005 — Contextual Branch Regime State]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001 / H0001 Logic Repair Audit]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
