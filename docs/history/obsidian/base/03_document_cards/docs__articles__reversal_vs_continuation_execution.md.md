---
title: "Article — Reversal vs Continuation Execution"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/articles/reversal_vs_continuation_execution.md"
source_ext: ".md"
category: "article_docs"
source_size_bytes: "2762"
entities:
  - "E0001"
  - "E0002"
  - "E0003"
  - "E0004"
  - "E0005"
  - "H0005"
concepts:
  - "Convexity"
  - "Execution"
  - "Structural Nodes"
  - "Validation"
---


# Article — Reversal vs Continuation Execution

**Source:** [[docs/articles/reversal_vs_continuation_execution|docs/articles/reversal_vs_continuation_execution.md]]

**Category:** `article_docs`  
**Status:** ok  
**Size:** `2762` bytes

## خلاصه

Reversal and continuation are not two names for the same edge. They describe different market behaviors and require different execution logic. This article summarizes the execution lessons learned from H0005. A reversal setup asks whether a structural zone can create a reaction when price revisits it. Important properties: entry is usually a zone touch, the edge may be short-lived, full structural targets can be too ambitious, same-bar target/stop ambiguity can be high on larger timeframes, costs and fill price matter heavily. A reversal report must therefore include: touch-based entry, zone-edge or structural invalidation stop, fixed R or first-opposite-zone target, same-bar policy, spread-

## Headings

- Article — Reversal vs Continuation Execution
-   Abstract
-   Reversal is a reaction problem
-   Continuation is a path problem
-   Why old continuation PF was not enough
-   Recommended execution split
-     Reversal family
-     Continuation family
-   Final rule

## Entities

`E0001`, `E0002`, `E0003`, `E0004`, `E0005`, `H0005`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/06_production/EXECUTION_FAMILIES/README|Execution Families]] — `production_signal`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
