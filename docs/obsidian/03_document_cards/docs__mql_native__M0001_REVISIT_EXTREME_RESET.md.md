---
title: "M0001 Revisit Extreme Reset"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_REVISIT_EXTREME_RESET.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1708"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 Revisit Extreme Reset

**Source:** [[docs/mql_native/M0001_REVISIT_EXTREME_RESET|docs/mql_native/M0001_REVISIT_EXTREME_RESET.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1708` bytes

## خلاصه

A revisited live node is not measured forever from the original node origin. After a confirmed revisit in HUNT mode, the node remains alive with memory, but its next expansion/territory cycle resets. The node is still the same structural node, but the market has already tested its territory. For the next revisit, we want to know the expansion from the last confirmed visit forward, not from the original node candle. Before any confirmed revisit: When: the visit is confirmed. If the node is not consumed: Then the next territory is built from that reset extreme. TOUCH mode consumes after the first confirmed touch, so there is no post-touch revisit cycle. If HUNT happens before confirmation, the

## Headings

- M0001 Revisit Extreme Reset
-   Decision
-   Why
-   First cycle
-   After each confirmed revisit in HUNT mode
-   TOUCH mode
-   Visual
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS|M0001 Node-Origin Zones and Revisit Text Colors]] — `mql_native_docs`
- [[docs/mql_native/M0001_REVISITED_LIVE_MEMORY|M0001 Revisited Live Memory]] — `mql_native_docs`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001 RTV — Log High/Low Volatility]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
