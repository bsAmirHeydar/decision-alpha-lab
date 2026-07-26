---
title: "M0001 Node Price Labels"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_NODE_PRICE_LABELS.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "796"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "NDS Anatomy"
---


# M0001 Node Price Labels

**Source:** [[docs/mql_native/M0001_NODE_PRICE_LABELS|docs/mql_native/M0001_NODE_PRICE_LABELS.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `796` bytes

## خلاصه

`InpShowNodePrices` no longer draws full-chart horizontal lines. It now draws a local text label near the node marker: HIGH node: price text above the red chevron LOW node: price text below the green chevron This keeps the chart clean while still showing the exact node price. The old full-chart line behavior is still available separately: Default: Full horizontal node-price lines create visual noise and can make structural inspection harder on M1/M5 charts. Local labels keep the chart readable and make each node's exact price obvious.

## Headings

- M0001 Node Price Labels
-   Change
-   Inputs
-   Reason

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_ARROW_MARKERS|M0001 Clean Arrow Markers]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/mql_native/M0001_DISABLE_NODE_PRICE_LINES|M0001 Disable Node Price Lines]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR|M0001 Exit-Gap Both-Sides Repair]] — `mql_native_docs`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001 Fast Final-Only Runtime]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
