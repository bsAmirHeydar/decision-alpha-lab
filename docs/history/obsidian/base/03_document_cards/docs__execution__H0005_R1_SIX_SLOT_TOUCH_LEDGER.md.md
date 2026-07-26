---
title: "H0005 Reversal Structural-Target-Capped Execution — Build 1.25"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "12549"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
---


# H0005 Reversal Structural-Target-Capped Execution — Build 1.25

**Source:** [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `12549` bytes

## خلاصه

This document is the execution contract for `E0001_ReversalOneToOne.mq5`. The strategy is evaluated once per closed candle by default: `InpRefreshSetupsOnNewBarOnly = true` `InpManageOrdersEveryTick = false` `InpUseClosedBarsOnly = true` The current forming candle is excluded from structural/regime calculations so the touch zone is not mutated by the same candle that is about to trade it. Execution does not invent its own market logic. It reuses the hypothesis modules: M0001 builds node territories and node consumption/hunt state. M0002 builds the last completed branch outcome: reversal or continuation. E0001 only translates the active H0005 reversal state into pending limit orders. `InpRegi

## Headings

- H0005 Reversal Structural-Target-Capped Execution — Build 1.25
-   Execution cadence
-   Source of truth
-   Regime input modes
-   Node selection
-   Spread-aware order geometry
-   Trading-session filter
-   Reversal exit
-   Consumption
-   Diagnostics
-   H0005 research report
-     Directional memory

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[docs/articles/reversal_vs_continuation_execution|Article — Reversal vs Continuation Execution]] — `article_docs`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
