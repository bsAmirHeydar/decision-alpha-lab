---
title: "E0005 — Continuation Close-Break Fixed-R Executor"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "2145"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "E0005"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0005 — Continuation Close-Break Fixed-R Executor

**Source:** [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `2145` bytes

## خلاصه

E0005 is the fifth H0005 execution module. It is a separate Expert Advisor. It does not modify E0001, E0002, E0003, or E0004. E0005 trades only the continuation side of H0005. A signal is valid when: 1. The local M0002 regime is continuation. 2. The latest fully closed candle breaks a confirmed structural node by close. 3. The node was active before the signal candle. 4. The same node was not already close-broken before the signal candle. 5. The node is not already consumed by a M0001 event. 6. Optional higher-timeframe regime filter passes. Close above a confirmed HIGH node = bullish continuation = market buy. Close below a confirmed LOW node = bearish continuation = market sell. The stop d

## Headings

- E0005 — Continuation Close-Break Fixed-R Executor
-   Contract
-   Direction
-   Risk and target
-   No-future behavior
-   Higher-timeframe filter

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `E0005`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
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
