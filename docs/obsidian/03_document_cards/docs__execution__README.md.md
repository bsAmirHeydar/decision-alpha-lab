---
title: "Decision Alpha Lab — Execution"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/README.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "5747"
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


# Decision Alpha Lab — Execution

**Source:** [[docs/execution/README|docs/execution/README.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `5747` bytes

## خلاصه

Canonical execution root: There must not be a nested `decision-alpha-lab/decision-alpha-lab` source copy. `E0001_ReversalOneToOne.mq5` implements H0005 reversal fixed-R execution. Current E0001 builds run once per closed candle, resolve the effective reversal/continuation regime from M0002 plus optional human context input, and park spread-aware pending limits on the nearest active reversal nodes: 3 nearest buy limits from LOW nodes below market by default. 3 nearest sell limits from HIGH nodes above market by default. SL is behind the zone. TP defaults to the first opposite-node touch; `InpRewardR` is an optional reference/cap when enabled. Continuation/non-reversal deletes managed pending

## Headings

- Decision Alpha Lab — Execution
-   Current execution adapter
-   MetaEditor include sync
-   Build 1.20 — strict touch/revisit ledger
-     Build 1.21 node-zone lock note
-   TP policy — first opposite node touch with optional R exit
-     Build 1.24 TP correction
-     Build 1.25 performance/compile fix
-   Minimal input surface
-   Higher-timeframe regime filter

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
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
