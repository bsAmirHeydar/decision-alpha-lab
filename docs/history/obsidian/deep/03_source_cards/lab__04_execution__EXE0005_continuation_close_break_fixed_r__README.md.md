
---
type: source_card
source_path: "lab/04_execution/EXE0005_continuation_close_break_fixed_r/README.md"
source_ext: ".md"
source_size: 860
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk"]
entities: ["E0003", "E0005", "EXE0005", "H0005", "M0002"]
---

# Source Card — README.md

## Source

[[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|lab/04_execution/EXE0005_continuation_close_break_fixed_r/README.md]]

## Summary

This execution module tests the clean continuation idea separately from trailing/regime-exit models. It enters after a confirmed structural node is broken by candle close while the H0005/M0002 regime is continuation. E0005 is intentionally different from E0003. E0003 can be a trailing/regime-exit continuation executor. E0005 is a fixed-reward continuation executor, designed for clean statistical comparison of continuation close-break entries with fixed R exits.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]

## Entities

E0003, E0005, EXE0005, H0005, M0002

## Headings

- EXE0005 — Continuation Close-Break Fixed-R
  - Purpose
  - Main idea
  - Main inputs
  - Notes

## Related Source Documents

- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `24`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `19`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `19`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `19`
- [[docs/execution/README|README.md]] — score `19`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `19`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `19`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `19`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `19`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
