---
title: "EXE0001 — H0005 Reversal Fixed-R Executor"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_execution/EXE0001_reversal_one_to_one/README.md"
source_ext: ".md"
category: "execution"
source_size_bytes: "5389"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "EXE0001"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# EXE0001 — H0005 Reversal Fixed-R Executor

**Source:** [[lab/04_execution/EXE0001_reversal_one_to_one/README|lab/04_execution/EXE0001_reversal_one_to_one/README.md]]

**Category:** `execution`  
**Status:** ok  
**Size:** `5389` bytes

## خلاصه

Build: `1.18` Purpose: execute the H0005 reversal branch as pending limit orders, not market chasing. On each closed candle: 1. Load bars from the configured symbol/timeframe. 2. Exclude the current forming candle by default. 3. Detect structural nodes through the existing L-rule/M0001 modules. 4. Compute M0001 events and the latest completed M0002 branch sample. 5. Resolve the effective regime: last completed branch only, or last branch combined with explicit human context input. 6. If reversal: place/update nearest LOW-node buy limits below market; place/update nearest HIGH-node sell limits above market. 7. If continuation/non-reversal: delete managed pending orders. LOW node buy: HIGH nod

## Headings

- EXE0001 — H0005 Reversal Fixed-R Executor
-   Contract
-   Defaults
-   Geometry
-   Optional time filter
-   H5 comparison report
-   Build 1.20 — strict touch/revisit ledger
-     Build 1.21 node-zone lock note
-   TP policy
-   Build 1.25 performance defaults
-   Minimal input surface
-   Higher-timeframe regime filter

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `EXE0001`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|EXE0005 — Continuation Close-Break Fixed-R]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
