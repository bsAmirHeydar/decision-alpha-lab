---
title: "E0003 — H0005 Continuation Close-Hunt Market Executor"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/E0003_CONTINUATION_CLOSE_HUNT.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "7599"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "Astro ML"
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0003 — H0005 Continuation Close-Hunt Market Executor

**Source:** [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|docs/execution/E0003_CONTINUATION_CLOSE_HUNT.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `7599` bytes

## خلاصه

`E0003_ContinuationCloseHunt.mq5` is the third execution adapter for Decision Alpha Lab. It is separate from `E0001` and `E0002`. Build 1.06 adds a selectable Donchian trigger policy: immediate intrabar tick breakout or closed-bar confirmation. When the effective continuation gate passes: 1. The EA waits for a **closed candle**. 2. Entry can use either: `E0003_ENTRY_CLOSE_HUNTED_NODE`: a structural node close-hunt. `E0003_ENTRY_DONCHIAN_BREAKOUT`: Donchian breakout, default period 20, with selectable trigger policy. 3. Close-hunt model: `HIGH` node close-hunt: `close > node.price + buffer` → buy continuation. `LOW` node close-hunt: `close < node.price - buffer` → sell continuation. 4. Donchi

## Headings

- E0003 — H0005 Continuation Close-Hunt Market Executor
-   Contract
-   Why the SL exists
-   Minimal inputs
-   Logs
-   Higher-timeframe regime filter
-   Build 1.02: ATR trailing and optional regime exit
-   Build 1.03: lower-timeframe regime gate and Donchian entry
-   Build 1.04: max trades and HTF direction control
-   Build 1.05: intrabar Donchian market trigger
-   Build 1.06: selectable Donchian trigger policy

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
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
