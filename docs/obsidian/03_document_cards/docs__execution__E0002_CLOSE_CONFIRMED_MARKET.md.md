---
title: "E0002 — H0005 Close-Confirmed Market Executor"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/E0002_CLOSE_CONFIRMED_MARKET.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "5139"
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
  - "Structural Nodes"
---


# E0002 — H0005 Close-Confirmed Market Executor

**Source:** [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|docs/execution/E0002_CLOSE_CONFIRMED_MARKET.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `5139` bytes

## خلاصه

`E0002_CloseConfirmedMarket.mq5` is a separate Expert Advisor from `E0001_ReversalOneToOne.mq5`. It does **not** add a mode to E0001 and does not modify the limit-on-touch executor. E0002 uses the same hypothesis modules as the rest of Decision Alpha Lab: M0001 structural nodes/events are the source of zones and node lifecycle. M0002 completed branch samples are the source of reversal/continuation regime. The optional human-context input can override or block the completed-branch regime gate. On each new closed candle, if the effective regime is reversal, E0002 checks the nearest active H5 reversal nodes: LOW nodes below market are buy candidates. HIGH nodes above market are sell candidates.

## Headings

- E0002 — H0005 Close-Confirmed Market Executor
-   Execution contract
-   Close-confirmed market entry
-     Buy from LOW node
-     Sell from HIGH node
-   Touch/revisit ledger
-   Session behavior
-   Managed identity
-   Build 1.03 compile and speed fix
-   Minimal input surface
-   Higher-timeframe regime filter

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
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
