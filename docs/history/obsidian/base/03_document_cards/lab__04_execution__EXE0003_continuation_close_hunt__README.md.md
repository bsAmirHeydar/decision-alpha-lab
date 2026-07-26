---
title: "EXE0003 — Continuation Close-Hunt Market Execution"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_execution/EXE0003_continuation_close_hunt/README.md"
source_ext: ".md"
category: "execution"
source_size_bytes: "5562"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "EXE0003"
  - "M0001"
  - "M0002"
concepts:
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# EXE0003 — Continuation Close-Hunt Market Execution

**Source:** [[lab/04_execution/EXE0003_continuation_close_hunt/README|lab/04_execution/EXE0003_continuation_close_hunt/README.md]]

**Category:** `execution`  
**Status:** ok  
**Size:** `5562` bytes

## خلاصه

This lab contains the third H5 execution path: regime: continuation trigger: structural node close-hunt or Donchian 20 breakout entry: market on the next bar position size: cash risk to `3 × ATR` stop distance by default TP: none primary exit: regime change Recommended first test: All four execution experts now support an optional higher-timeframe regime gate. The default is off, so existing tests are unchanged. Inputs: `InpUseHigherTimeframeRegimeFilter` — enable/disable the higher-timeframe regime confirmation. `InpHigherRegimeTimeframe` — timeframe used for the higher-timeframe M0001/M0002 regime calculation, default `PERIOD_H1`. `InpUseHigherTimeframeDirectionFilter` — when false, the hi

## Headings

- EXE0003 — Continuation Close-Hunt Market Execution
-   Higher-timeframe regime filter
-   Build 1.02: ATR trailing and optional regime exit
-   Build 1.03: Donchian 20 and optional lower-timeframe regime gate
-   Build 1.04: max trades and HTF direction control
-   Build 1.05: intrabar Donchian market trigger
-   Build 1.06: selectable Donchian trigger policy

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `EXE0003`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`
- [[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|EXE0005 — Continuation Close-Break Fixed-R]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
