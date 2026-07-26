---
title: "M0001 MQL-Native Specification"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_MQL_NATIVE_SPEC.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "897"
entities:
  - "M0001"
concepts:
  - "NDS Anatomy"
---


# M0001 MQL-Native Specification

**Source:** [[docs/mql_native/M0001_MQL_NATIVE_SPEC|docs/mql_native/M0001_MQL_NATIVE_SPEC.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `897` bytes

## خلاصه

A node at index `i` is confirmed only when `L` right-side candles exist. For `L = 5`: The node is available in a live-safe stream when: The visual marker is drawn on the pivot candle, not on the confirmation candle. For each confirmed node: 1. Start scanning from `active_from_index = node_index + L`. 2. Expand the opposite extreme. 3. Build a territory around the node price. 4. Start an event when a candle intersects the territory. 5. Close the event after `exit_gap` outside candles. 6. Compute: The native Expert reads candles directly from MT5. No external bridge, file watcher, or asynchronous process is involved.

## Headings

- M0001 MQL-Native Specification
-   L-rule node
-   RTV event
-   Runtime Guarantee

## Entities

`M0001`

## Concepts

- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_ARROW_ANCHOR_COMPILE_FIX|M0001 Arrow Anchor Compile Fix]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_ARROW_MARKERS|M0001 Clean Arrow Markers]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_EXTREME_HISTORY|M0001 Consumed Extreme History]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
