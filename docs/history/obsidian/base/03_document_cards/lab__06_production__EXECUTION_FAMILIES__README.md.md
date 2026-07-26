---
title: "Execution Families"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/06_production/EXECUTION_FAMILIES/README.md"
source_ext: ".md"
category: "production_signal"
source_size_bytes: "1616"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "E0005"
concepts:
  - "Execution"
  - "Known-Time Causality"
  - "Structural Nodes"
  - "Validation"
---


# Execution Families

**Source:** [[lab/06_production/EXECUTION_FAMILIES/README|lab/06_production/EXECUTION_FAMILIES/README.md]]

**Category:** `production_signal`  
**Status:** ok  
**Size:** `1616` bytes

## خلاصه

This document summarizes the current execution families implied by the research. Purpose: capture reaction from structural zones. Expected members: E0001 — reversal touch/limit execution, E0002 — close-confirmed market reversal execution. Core rules: entry after valid regime is known, zone touch or close confirmation, zone-edge or structural invalidation stop, fixed R or first opposite zone target, same-bar stop-first policy unless tick data proves ordering. Main risk: full structural reversal targets can be too ambitious, same-bar target/stop ambiguity can be high, costs can destroy small reaction edges. Purpose: capture larger path after structural break in continuation regime. Expected me

## Headings

- Execution Families
-   Reversal execution family
-   Continuation execution family
-   Family-level reporting

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `E0005`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[docs/articles/reversal_vs_continuation_execution|Article — Reversal vs Continuation Execution]] — `article_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|EXE0005 — Continuation Close-Break Fixed-R]] — `execution`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
