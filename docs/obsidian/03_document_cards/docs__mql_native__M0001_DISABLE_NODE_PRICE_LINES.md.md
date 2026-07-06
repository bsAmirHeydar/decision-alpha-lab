---
title: "M0001 Disable Node Price Lines"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_DISABLE_NODE_PRICE_LINES.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "734"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "NDS Anatomy"
  - "Validation"
---


# M0001 Disable Node Price Lines

**Source:** [[docs/mql_native/M0001_DISABLE_NODE_PRICE_LINES|docs/mql_native/M0001_DISABLE_NODE_PRICE_LINES.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `734` bytes

## خلاصه

Full-chart horizontal node price lines are now hard-disabled. Even if `InpShowNodePriceLines` is accidentally left `true` in an old MT5 input set, the Expert forces: and the visual module no longer calls `DAL_DrawHLine()` for node prices. Use local text labels: This draws: HIGH node price above the high-node arrow LOW node price below the low-node arrow Full horizontal lines create heavy chart noise and make node inspection harder. M0001 visual validation should show local node information, not permanent full-chart levels for every node.

## Headings

- M0001 Disable Node Price Lines
-   Change
-   Correct way to show node prices
-   Reason

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001 Fast Final-Only Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_PROJECT_REPORT_SYNC|M0001 Project Report Sync]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
