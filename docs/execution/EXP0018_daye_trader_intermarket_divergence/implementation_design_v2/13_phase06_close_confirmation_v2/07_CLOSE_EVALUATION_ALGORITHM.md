---
id: EXP0018-P06-ALGORITHM
title: "P06 Close Evaluation Algorithm"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Algorithm

1. Refresh P05.
2. Read exact current and latest closed host bars for both symbols.
3. Detect host-close advancement.
4. Compare current P05 observations with prior source memory.
5. Open candidates only on live one-sided transitions.
6. Update pending candidates only with source availability at or before their target close.
7. On a new host close, finalize every candidate targeting that exact host bar.
8. Remember the finalized observation identity before processing another callback.
9. Persist pending and finalized identity state.
10. Emit typed event, result, diagnostics, and optional audit rows.
