---
title: "EXE0002 — Close-Confirmed Market After Touch"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_execution/EXE0002_close_confirmed_market/README.md"
source_ext: ".md"
category: "execution"
source_size_bytes: "2969"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "EXE0002"
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


# EXE0002 — Close-Confirmed Market After Touch

**Source:** [[lab/04_execution/EXE0002_close_confirmed_market/README|lab/04_execution/EXE0002_close_confirmed_market/README.md]]

**Category:** `execution`  
**Status:** ok  
**Size:** `2969` bytes

## خلاصه

This execution experiment is the second implementation of the H0005 reversal idea. It is intentionally a separate EA: It does not add a mode to `E0001_ReversalOneToOne.mq5`. When the effective regime is reversal: 1. Build H5 reversal node candidates from M0001/M0002. 2. Watch nearest LOW nodes below market and HIGH nodes above market. 3. Wait for the last closed candle to touch a candidate zone. 4. If the close does not break the far edge of the zone, enter at market. 5. Put SL behind the zone. 6. Put TP at the first opposite-node touch by default. `InpRewardR` is a reference/cap only if `InpUseFixedRExitIfCloser=true`. 7. Lock that node touch until a full zone exit and later revisit. TP def

## Headings

- EXE0002 — Close-Confirmed Market After Touch
-   Rule
-   Recommended default test settings
-   TP policy
-   Build 1.03 performance defaults
-   Minimal input surface
-   Higher-timeframe regime filter

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `EXE0002`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|EXE0005 — Continuation Close-Break Fixed-R]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
