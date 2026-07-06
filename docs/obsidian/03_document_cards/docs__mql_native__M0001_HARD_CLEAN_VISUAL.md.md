---
title: "M0001 Hard Clean Visual"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_HARD_CLEAN_VISUAL.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "993"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "MQL Native"
  - "NDS Anatomy"
---


# M0001 Hard Clean Visual

**Source:** [[docs/mql_native/M0001_HARD_CLEAN_VISUAL|docs/mql_native/M0001_HARD_CLEAN_VISUAL.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `993` bytes

## خلاصه

The chart still showed red/blue lines tracking candle highs/lows. These lines were not part of the desired node output. Desired node output: No high/low trace lines, no chevron wings, no indicator traces. The Expert now has hard cleanup controls: `InpPurgeTraceLines` deletes trend/channel style chart objects on every redraw. `InpPurgeMainWindowIndicators` removes main-window indicators on init, useful when ZigZag-style traces remained attached to the chart. Node price labels now use separate gaps: This moves high labels higher and low labels lower for readability. `M0001_LiveVisualLab.mq5` version: `1.15`.

## Headings

- M0001 Hard Clean Visual
-   Problem
-   Fix
-   Price label spacing
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001 Minimal Inputs]] — `mql_native_docs`
- [[docs/mql_native/M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS|M0001 Node-Origin Zones and Revisit Text Colors]] — `mql_native_docs`
- [[docs/mql_native/M0001_PROJECT_REPORT_SYNC|M0001 Project Report Sync]] — `mql_native_docs`
- [[docs/mql_native/M0001_REVISIT_EXTREME_RESET|M0001 Revisit Extreme Reset]] — `mql_native_docs`
- [[docs/mql_native/M0001_REVISITED_LIVE_MEMORY|M0001 Revisited Live Memory]] — `mql_native_docs`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001 RTV — Log High/Low Volatility]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
