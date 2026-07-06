---
title: "M0001 Live Bar Stream"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_LIVE_BAR_STREAM.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1521"
entities:
  - "M0001"
concepts:
  - "Convexity"
  - "NDS Anatomy"
  - "Validation"
---


# M0001 Live Bar Stream

**Source:** [[docs/mql_native/M0001_LIVE_BAR_STREAM|docs/mql_native/M0001_LIVE_BAR_STREAM.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1521` bytes

## خلاصه

The first MQL-native version recomputed the engine by loading a whole bar window with `CopyRates()` on every update. That is convenient for research snapshots, but it does not express the strict live mental model: The active M0001 Expert now runs in live-stream mode by default. This means: 1. The Expert does not bulk-copy history at attach time. 2. It waits for the next newly closed candle. 3. On each new closed candle, it reads only `shift=1`. 4. That single bar is appended to the in-memory chronological stream. 5. L-rule nodes, M0001 events, and visuals are recomputed from that live stream. `InpBars` is now the rolling stream capacity, not a bulk-copy request, when `InpUseLiveBarStream=tru

## Headings

- M0001 Live Bar Stream
-   Problem
-   Decision
-   Inputs
-   Optional warmup
-   Fallback mode

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001 Consumed Node Repair]] — `mql_native_docs`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001 Fast Final-Only Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001 Professional Validation Metrics — v1.60]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
