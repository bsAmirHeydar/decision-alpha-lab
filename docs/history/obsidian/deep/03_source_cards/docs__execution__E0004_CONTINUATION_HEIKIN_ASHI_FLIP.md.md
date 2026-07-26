
---
type: source_card
source_path: "docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md"
source_ext: ".md"
source_size: 3263
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "M0001", "M0002"]
---

# Source Card — E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md

## Source

[[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]]

## Summary

`E0004_ContinuationHeikinAshiFlip.mq5` is the fourth execution adapter for Decision Alpha Lab. It is intentionally separate from E0001, E0002, and E0003. E0004 only searches for entries when the effective regime is `CONTINUATION`. On each new closed candle it calculates Heikin Ashi candles from the same closed-bar stream used by the existing M0001/M0002 modules. A signal exists when: The current closed Heikin Ashi candle has a non-doji color. The previous closed Heikin Ashi candle has the opposite non-doji color. The current Heikin Ashi color is in the inferred continuation direction. The continuation direction is inferred from the most recent structural close-hunt: close above a confirmed HIGH node means bullish continuation direction. close below a confirmed LOW node means bearish continuation direction. Bullish HA flip in bullish continuation direction: Buy Market. Bearish HA flip in

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, M0001, M0002

## Headings

- E0004 — Continuation Heikin Ashi Flip Executor
  - Contract
  - Orders
  - Simultaneous trades
  - Minimal inputs
  - Notes
  - Build 1.01 stop update
  - Higher-timeframe regime filter

## Related Source Documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `43`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `43`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `43`
- [[docs/execution/README|README.md]] — score `43`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `42`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `40`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `39`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `38`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `38`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `28`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
