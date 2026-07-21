---
title: "E0004 — Continuation Heikin Ashi Flip Executor"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "3263"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "M0001"
  - "M0002"
concepts:
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0004 — Continuation Heikin Ashi Flip Executor

**Source:** [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `3263` bytes

## خلاصه

`E0004_ContinuationHeikinAshiFlip.mq5` is the fourth execution adapter for Decision Alpha Lab. It is intentionally separate from E0001, E0002, and E0003. E0004 only searches for entries when the effective regime is `CONTINUATION`. On each new closed candle it calculates Heikin Ashi candles from the same closed-bar stream used by the existing M0001/M0002 modules. A signal exists when: 1. The current closed Heikin Ashi candle has a non-doji color. 2. The previous closed Heikin Ashi candle has the opposite non-doji color. 3. The current Heikin Ashi color is in the inferred continuation direction. The continuation direction is inferred from the most recent structural close-hunt: close above a co

## Headings

- E0004 — Continuation Heikin Ashi Flip Executor
-   Contract
-   Orders
-   Simultaneous trades
-   Minimal inputs
-   Notes
-   Build 1.01 stop update
-   Higher-timeframe regime filter

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[docs/articles/reversal_vs_continuation_execution|Article — Reversal vs Continuation Execution]] — `article_docs`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
