---
title: "M0001 Revisited Live Memory"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_REVISITED_LIVE_MEMORY.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "2027"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 Revisited Live Memory

**Source:** [[docs/mql_native/M0001_REVISITED_LIVE_MEMORY|docs/mql_native/M0001_REVISITED_LIVE_MEMORY.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `2027` bytes

## خلاصه

A revisit does not have to happen immediately after the previous event. In HUNT consumption mode, a confirmed touch does not kill the node. The node returns to normal tracking and can be revisited much later. A node is fresh while it is alive and has no confirmed revisit: Visual label: In TOUCH mode: When price enters the live territory zone, the next revisit starts: Visual label: In TOUCH mode: A pending revisit becomes confirmed only after: In HUNT mode, confirmation stores memory and returns the node to tracking: The next revisit can happen many candles later. Visual label: `age` is the number of bars since the last confirmed revisit. In TOUCH mode: There is no true multi-revisit loop in

## Headings

- M0001 Revisited Live Memory
-   Core idea
-   Fresh live node
-   Pending revisit
-   Confirmed revisit
-   Consumption
-   Why this matters
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS|M0001 Node-Origin Zones and Revisit Text Colors]] — `mql_native_docs`
- [[docs/mql_native/M0001_REVISIT_EXTREME_RESET|M0001 Revisit Extreme Reset]] — `mql_native_docs`
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
