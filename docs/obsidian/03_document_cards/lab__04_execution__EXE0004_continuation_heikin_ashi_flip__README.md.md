---
title: "EXE0004 — Continuation Heikin Ashi Flip"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README.md"
source_ext: ".md"
category: "execution"
source_size_bytes: "1896"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "EXE0004"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
---


# EXE0004 — Continuation Heikin Ashi Flip

**Source:** [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README.md]]

**Category:** `execution`  
**Status:** ok  
**Size:** `1896` bytes

## خلاصه

Fourth execution adapter for the H0005 continuation side. When the market regime is continuation, use Heikin Ashi color flips as repeated entries in the continuation direction. On each closed candle: 1. regime = continuation; 2. current HA candle color differs from previous HA candle color; 3. current HA color agrees with the inferred continuation direction; 4. enter at market. Fixed reward model: SL: opposite edge of the signal Heikin Ashi candle; TP: `InpRewardR`, default `2.0R`. `InpAllowSimultaneousTrades` decides whether repeated signals can stack positions or whether only one E0004 position can be open at a time. The stop is no longer only the signal Heikin Ashi candle edge. For buys,

## Headings

- EXE0004 — Continuation Heikin Ashi Flip
-   Idea
-   Signal
-   Exit
-   Simultaneous trades
-   Build 1.01 stop update
-   Higher-timeframe regime filter

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `EXE0004`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`
- [[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|EXE0005 — Continuation Close-Break Fixed-R]] — `execution`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
